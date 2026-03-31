
"""
capstone_streamlit.py — FitGuide Health & Fitness Advisor
Run: streamlit run capstone_streamlit.py
"""
import streamlit as st
import uuid
import os
import chromadb
from dotenv import load_dotenv
from typing import TypedDict, List
from sentence_transformers import SentenceTransformer
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

st.set_page_config(
    page_title="FitGuide — Health & Fitness Advisor",
    page_icon="💪",
    layout="centered"
)
st.title("💪 FitGuide — Health & Fitness Advisor")
st.caption("Evidence-based fitness and nutrition guidance for all ages, powered by AI.")

@st.cache_resource
def load_agent():
    llm      = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    embedder = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.Client()
    try: client.delete_collection("capstone_kb")
    except: pass
    collection = client.create_collection("capstone_kb")

    DOCUMENTS = [
        {"id":"doc_001","topic":"Caloric Balance and Weight Management","text":"""Weight management is fundamentally governed by the principle of caloric balance. A deficit of approximately 500 calories per day typically produces about 0.5 kg of weight loss per week. A moderate deficit of 300–500 calories below TDEE is the evidence-based sweet spot for sustained fat loss without muscle sacrifice."""},
        {"id":"doc_002","topic":"Macronutrients: Protein, Carbohydrates, and Fats","text":"""Protein (4 kcal/g) is essential for muscle repair. Active individuals benefit from 1.2–2.0 g/kg body weight. Carbohydrates are the body's preferred fuel. Complex carbs (oats, brown rice, legumes) provide sustained energy. Fats (9 kcal/g) are vital for hormone production and vitamin absorption. Healthy sources include avocado, olive oil, and nuts."""},
        {"id":"doc_003","topic":"Hydration and Water Intake","text":"""General guidelines recommend 2.7 litres per day for women and 3.7 litres per day for men from all sources. Pale yellow urine indicates good hydration. Sports drinks are beneficial during exercise exceeding 60–90 minutes."""},
        {"id":"doc_004","topic":"Cardiovascular Exercise and Heart Health","text":"""WHO recommends 150–300 minutes of moderate-intensity aerobic activity or 75–150 minutes of vigorous activity per week. Moderate intensity corresponds to 50–70% of maximum heart rate (220 minus age)."""},
        {"id":"doc_005","topic":"Strength Training and Muscle Building","text":"""For hypertrophy: 3–5 sets of 8–12 reps at 65–85% of 1RM with 60–90 seconds rest. Beginners should start with compound movements. Protein intake post-workout supports muscle protein synthesis."""},
        {"id":"doc_006","topic":"Sleep and Recovery for Fitness","text":"""Adults require 7–9 hours per night. During deep sleep, 70–80% of daily growth hormone is released, driving muscle repair. Sleep deprivation elevates cortisol and increases caloric intake by 300–400 calories per day."""},
        {"id":"doc_007","topic":"Healthy Eating Patterns and Meal Timing","text":"""Fill half your plate with vegetables and fruit. Limit added sugars to 25g/day for women, 36g/day for men. Spreading protein across 3–5 meals maximises muscle protein synthesis. Intermittent fasting is not superior to continuous restriction when calories are matched."""},
        {"id":"doc_008","topic":"BMI, Body Composition, and Healthy Weight Ranges","text":"""BMI categories: Underweight < 18.5, Normal 18.5–24.9, Overweight 25–29.9, Obese >= 30. BMI does not distinguish fat from muscle. Waist circumference risk increases above 80 cm for women, 94 cm for men."""},
        {"id":"doc_009","topic":"Stress Management and Mental Wellness in Fitness","text":"""Chronic stress elevates cortisol promoting fat storage and muscle breakdown. Exercise reduces cortisol, increases endorphins, and reduces anxiety and depression. Even 10 minutes of daily meditation reduces perceived stress over 8 weeks."""},
        {"id":"doc_010","topic":"Common Fitness Myths and Misconceptions","text":"""Spot reduction does not work — fat loss is systemic. Resistance training builds muscle which raises resting metabolic rate. Dietary fat does not directly cause body fat accumulation. Static stretching before exercise reduces power; dynamic warm-up is better pre-workout."""},
        {"id":"doc_011","topic":"Nutrition for Different Life Stages","text":"""Older adults need 1.2–1.6 g/kg protein daily to combat sarcopenia. Pregnant women need 300 extra kcal/day in the second and third trimesters. Folate, iron, calcium, and iodine are critical during pregnancy."""},
        {"id":"doc_012","topic":"Creating a Sustainable Fitness Routine","text":"""A balanced beginner week: 2–3 strength sessions, 2–3 cardio sessions, 1–2 rest days. Aim for 80% adherence rather than perfection. Workout partners or group classes improve long-term consistency by 30–50%."""},
    ]
    texts = [d["text"] for d in DOCUMENTS]
    collection.add(
        documents=texts,
        embeddings=embedder.encode(texts).tolist(),
        ids=[d["id"] for d in DOCUMENTS],
        metadatas=[{"topic": d["topic"]} for d in DOCUMENTS]
    )

    class CapstoneState(TypedDict):
        question: str
        messages: List[dict]
        route: str
        retrieved: str
        sources: List[str]
        tool_result: str
        answer: str
        faithfulness: float
        eval_retries: int
        search_results: str

    def memory_node(state):
        msgs = state.get("messages", []) + [{"role":"user","content":state["question"]}]
        return {"messages": msgs[-6:]}

    def router_node(state):
        prompt = f"""Router for Health & Fitness Advisor.
Options: retrieve / memory_only / tool (web search for latest research/news)
Question: {state["question"]}
Reply ONE word only."""
        dec = llm.invoke(prompt).content.strip().lower()
        if "memory" in dec: dec = "memory_only"
        elif "tool" in dec: dec = "tool"
        else: dec = "retrieve"
        return {"route": dec}

    def retrieval_node(state):
        emb = embedder.encode([state["question"]]).tolist()
        res = collection.query(query_embeddings=emb, n_results=3)
        topics = [m["topic"] for m in res["metadatas"][0]]
        ctx = "\n\n---\n\n".join(f"[{topics[i]}]\n{res["documents"][0][i]}" for i in range(len(topics)))
        return {"retrieved": ctx, "sources": topics}

    def skip_retrieval_node(state):
        return {"retrieved": "", "sources": []}

    def tool_node(state):
        try:
            from ddgs import DDGS
            with DDGS() as ddgs:
                results = list(ddgs.text(state["question"] + " health fitness", max_results=4))
            tr = "\n\n".join(f"{r.get("title","")}: {r.get("body","")[:300]}" for r in results) if results else "No results found."
        except Exception as e:
            tr = f"Web search unavailable: {e}"
        return {"tool_result": tr, "search_results": tr}

    def answer_node(state):
        ctx_parts = []
        if state.get("retrieved"): ctx_parts.append(f"KNOWLEDGE BASE:\n{state["retrieved"]}")
        if state.get("tool_result"): ctx_parts.append(f"WEB SEARCH:\n{state["tool_result"]}")
        ctx = "\n\n".join(ctx_parts)
        sys = f"""You are FitGuide, an evidence-based Health & Fitness Advisor for all ages.
Answer using ONLY the information below. If not available, say you don't have that info and recommend a professional.
Keep answers warm, clear, and actionable.
{ctx}""" if ctx else "You are FitGuide. Answer warmly from conversation history."
        msgs = [SystemMessage(content=sys)]
        for m in state.get("messages", [])[:-1]:
            msgs.append(HumanMessage(content=m["content"]) if m["role"]=="user" else AIMessage(content=m["content"]))
        msgs.append(HumanMessage(content=state["question"]))
        return {"answer": llm.invoke(msgs).content}

    def eval_node(state):
        ctx = state.get("retrieved","")[:500]
        if not ctx: return {"faithfulness": 1.0, "eval_retries": state.get("eval_retries",0)+1}
        try:
            score = float(llm.invoke(f"Rate faithfulness 0.0-1.0. Context: {ctx} Answer: {state.get("answer","")[:200]}").content.strip().split()[0])
            score = max(0.0, min(1.0, score))
        except: score = 0.5
        return {"faithfulness": score, "eval_retries": state.get("eval_retries",0)+1}

    def save_node(state):
        return {"messages": state.get("messages",[]) + [{"role":"assistant","content":state.get("answer","")}]}

    FAITHFULNESS_THRESHOLD = 0.7
    MAX_EVAL_RETRIES = 2

    def route_decision(state):
        r = state.get("route","retrieve")
        if r=="tool": return "tool"
        if r=="memory_only": return "skip"
        return "retrieve"

    def eval_decision(state):
        if state.get("faithfulness",1.0) >= FAITHFULNESS_THRESHOLD or state.get("eval_retries",0) >= MAX_EVAL_RETRIES: return "save"
        return "answer"

    g = StateGraph(CapstoneState)
    for name, fn in [("memory",memory_node),("router",router_node),("retrieve",retrieval_node),
                     ("skip",skip_retrieval_node),("tool",tool_node),("answer",answer_node),
                     ("eval",eval_node),("save",save_node)]:
        g.add_node(name, fn)
    g.set_entry_point("memory")
    g.add_edge("memory","router")
    g.add_conditional_edges("router", route_decision, {"retrieve":"retrieve","skip":"skip","tool":"tool"})
    for n in ["retrieve","skip","tool"]: g.add_edge(n,"answer")
    g.add_edge("answer","eval")
    g.add_conditional_edges("eval", eval_decision, {"answer":"answer","save":"save"})
    g.add_edge("save", END)
    agent_app = g.compile(checkpointer=MemorySaver())
    return agent_app, embedder, collection

try:
    agent_app, embedder, collection = load_agent()
    st.success(f"✅ Knowledge base loaded — {collection.count()} documents")
except Exception as e:
    st.error(f"Failed to load agent: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())[:8]

with st.sidebar:
    st.header("🥗 About FitGuide")
    st.write("Evidence-based fitness and nutrition guidance for all ages, powered by AI.")
    st.write(f"Session ID: `{st.session_state.thread_id}`")
    st.divider()
    st.write("**Topics covered:**")
    topics = ["Caloric Balance & Weight Management","Macronutrients","Hydration",
               "Cardio & Heart Health","Strength Training","Sleep & Recovery",
               "Healthy Eating Patterns","BMI & Body Composition","Stress & Mental Wellness",
               "Fitness Myths","Life-Stage Nutrition","Sustainable Routines"]
    for t in topics:
        st.write(f"• {t}")
    st.divider()
    if st.button("🗑️ New conversation"):
        st.session_state.messages = []
        st.session_state.thread_id = str(uuid.uuid4())[:8]
        st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask FitGuide about nutrition, exercise, weight loss..."):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role":"user","content":prompt})

    with st.chat_message("assistant"):
        with st.spinner("FitGuide is thinking..."):
            config = {"configurable": {"thread_id": st.session_state.thread_id}}
            result = agent_app.invoke({"question": prompt}, config=config)
            answer = result.get("answer", "Sorry, I could not generate an answer.")
        st.write(answer)
        faith  = result.get("faithfulness", 0.0)
        route  = result.get("route", "?")
        sources = result.get("sources", [])
        st.caption(f"Route: {route} | Faithfulness: {faith:.2f} | Sources: {sources}")

    st.session_state.messages.append({"role":"assistant","content":answer})

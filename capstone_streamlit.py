"""
capstone_streamlit.py — FitGuide Health & Fitness Advisor
Run: streamlit run capstone_streamlit.py
Author: Debdyuti Chakraborty (23051339)
"""

import streamlit as st
import uuid
import os
from dotenv import load_dotenv
from typing import TypedDict, List

load_dotenv()

# ── Page config ───────────────────────────────────────────
st.set_page_config(
    page_title="FitGuide — Health & Fitness Advisor",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root variables ── */
:root {
    --green:       #2D6A4F;
    --green-light: #40916C;
    --green-pale:  #D8F3DC;
    --green-mist:  #F0FAF2;
    --amber:       #E9C46A;
    --amber-dark:  #C9A227;
    --text:        #1B2D24;
    --text-soft:   #4A6155;
    --border:      #B7DFC5;
    --surface:     #FFFFFF;
    --bg:          #F5FBF7;
}

/* ── Base reset ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    font-family: 'DM Sans', sans-serif;
    color: var(--text) !important;
}

/* Force all regular text dark */
[data-testid="stMain"] p,
[data-testid="stMain"] li,
[data-testid="stMain"] span,
[data-testid="stMain"] label {
    color: var(--text) !important;
}

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1B2D24 0%, #2D6A4F 100%) !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * {
    color: #E8F5EC !important;
}
[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.12) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    color: white !important;
    border-radius: 8px !important;
    width: 100%;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    transition: all 0.2s ease;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.22) !important;
    transform: translateY(-1px);
}
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.15) !important;
}

/* ── Main content area ── */
[data-testid="stMain"] {
    background: var(--bg) !important;
}

/* ── Header banner ── */
.fitguide-header {
    background: linear-gradient(135deg, #1B2D24 0%, #2D6A4F 60%, #40916C 100%);
    border-radius: 20px;
    padding: 36px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.fitguide-header::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(233,196,106,0.18) 0%, transparent 70%);
    border-radius: 50%;
}
.fitguide-header::after {
    content: '';
    position: absolute;
    bottom: -60px; left: 20%;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(64,145,108,0.25) 0%, transparent 70%);
    border-radius: 50%;
}
.fitguide-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.6rem;
    color: #FFFFFF;
    margin: 0 0 6px 0;
    line-height: 1.1;
    position: relative; z-index: 1;
}
.fitguide-title span { color: var(--amber); }
.fitguide-subtitle {
    color: rgba(255,255,255,0.75);
    font-size: 1rem;
    font-weight: 300;
    margin: 0;
    position: relative; z-index: 1;
    letter-spacing: 0.3px;
}

/* ── Stats bar ── */
.stats-bar {
    display: flex;
    gap: 12px;
    margin-bottom: 24px;
    flex-wrap: wrap;
}
.stat-chip {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 50px;
    padding: 8px 18px;
    font-size: 0.82rem;
    font-weight: 500;
    color: var(--green);
    display: flex;
    align-items: center;
    gap: 7px;
    box-shadow: 0 1px 4px rgba(45,106,79,0.08);
}
.stat-chip .dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--green-light);
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.85); }
}

/* ── Chat container ── */
.chat-wrap {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 24px;
    margin-bottom: 16px;
    min-height: 420px;
    max-height: 560px;
    overflow-y: auto;
    box-shadow: 0 2px 16px rgba(45,106,79,0.06);
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    border-radius: 16px !important;
    padding: 4px 0 !important;
    margin-bottom: 4px !important;
}

/* Force dark text on ALL chat message content */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] ol,
[data-testid="stChatMessage"] ul,
[data-testid="stChatMessage"] strong,
[data-testid="stChatMessage"] em,
[data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] div {
    color: #1B2D24 !important;
}

/* User messages */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: #EAF6EE !important;
    border: 1px solid #B7DFC5 !important;
    padding: 14px 18px !important;
    border-radius: 18px 18px 4px 18px !important;
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) p,
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) span,
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) div {
    color: #1B2D24 !important;
    font-weight: 500 !important;
}

/* Assistant messages */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    background: #FFFFFF !important;
    border: 1.5px solid #B7DFC5 !important;
    padding: 16px 20px !important;
    border-radius: 18px 18px 18px 4px !important;
    box-shadow: 0 2px 12px rgba(45,106,79,0.10) !important;
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) p,
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) li,
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) strong,
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) span,
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) div {
    color: #1B2D24 !important;
    line-height: 1.7 !important;
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) strong {
    color: #2D6A4F !important;
    font-weight: 700 !important;
}

/* Also target the markdown container directly */
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] strong,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] ul,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] ol {
    color: #1B2D24 !important;
}

/* ── Input ── */
[data-testid="stChatInput"] {
    border-radius: 14px !important;
    border: 2px solid var(--border) !important;
    background: var(--surface) !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: border-color 0.2s;
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--green-light) !important;
    box-shadow: 0 0 0 3px rgba(64,145,108,0.12) !important;
}

/* ── Meta info badge ── */
.meta-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--green-mist);
    border: 1px solid var(--green-pale);
    border-radius: 8px;
    padding: 5px 12px;
    font-size: 0.75rem;
    color: var(--text-soft);
    margin-top: 8px;
    font-family: 'DM Sans', sans-serif;
}

/* ── Sidebar topic pills ── */
.topic-pill {
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 8px;
    padding: 5px 11px;
    font-size: 0.78rem;
    color: rgba(255,255,255,0.85) !important;
    margin-bottom: 5px;
    display: block;
}

/* ── Welcome card ── */
.welcome-card {
    background: linear-gradient(135deg, var(--green-mist), #FFFFFF);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px 28px;
    text-align: center;
    color: var(--text-soft);
}
.welcome-card h3 {
    font-family: 'DM Serif Display', serif;
    color: var(--green);
    margin-bottom: 10px;
    font-size: 1.4rem;
}

/* ── Suggestion chips ── */
.suggestion-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    margin-top: 16px;
}
.suggestion {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: 50px;
    padding: 7px 16px;
    font-size: 0.82rem;
    color: var(--green);
    cursor: pointer;
    transition: all 0.2s;
    font-weight: 500;
}
.suggestion:hover {
    background: var(--green-pale);
    border-color: var(--green-light);
}

/* ── Typing indicator ── */
.typing-indicator {
    display: flex;
    align-items: center;
    gap: 5px;
    padding: 10px 16px;
    background: var(--green-mist);
    border-radius: 12px;
    width: fit-content;
    margin: 4px 0;
}
.typing-indicator span {
    width: 7px; height: 7px;
    background: var(--green-light);
    border-radius: 50%;
    animation: bounce 1.2s infinite;
}
.typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
.typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce {
    0%, 60%, 100% { transform: translateY(0); }
    30% { transform: translateY(-6px); }
}

/* ── Route badge colours ── */
.route-retrieve { color: #2D6A4F; background: #D8F3DC; border-color: #B7DFC5; }
.route-tool     { color: #9B4DCA; background: #F3E8FF; border-color: #D8B4FE; }
.route-memory   { color: #C47A00; background: #FFF3CD; border-color: #FFE082; }

/* ── Scrollbar ── */
.chat-wrap::-webkit-scrollbar { width: 5px; }
.chat-wrap::-webkit-scrollbar-track { background: transparent; }
.chat-wrap::-webkit-scrollbar-thumb { background: var(--border); border-radius: 10px; }

/* ── Section divider ── */
.section-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.45);
    margin: 16px 0 8px 0;
}
</style>
""", unsafe_allow_html=True)


# ── Agent loader ──────────────────────────────────────────
@st.cache_resource(show_spinner="Loading FitGuide agent...")
def load_agent():
    from langchain_groq import ChatGroq
    from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
    from langgraph.graph import StateGraph, END
    from langgraph.checkpoint.memory import MemorySaver
    import chromadb
    from sentence_transformers import SentenceTransformer

    llm      = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    embedder = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.Client()
    try:
        client.delete_collection("fitguide_kb")
    except:
        pass
    collection = client.create_collection("fitguide_kb")

    DOCUMENTS = [
        {"id": "doc_001", "topic": "Caloric Balance and Weight Management",
         "text": """Weight management is fundamentally governed by the principle of caloric balance — the relationship between calories consumed and calories expended. When you consume more calories than your body burns, the surplus is stored as fat, leading to weight gain. Conversely, a caloric deficit — burning more than you eat — results in weight loss. A deficit of approximately 500 calories per day typically produces about 0.5 kg (1 lb) of weight loss per week, which is considered a safe and sustainable rate.

Total Daily Energy Expenditure (TDEE) combines your Basal Metabolic Rate (BMR), the thermic effect of food, and activity calories. BMR is the energy your body uses at rest to maintain basic functions like breathing, circulation, and cell repair. It accounts for 60–75% of total energy use.

Crash diets that create extreme caloric deficits (below 1200 kcal/day for women or 1500 for men) are counterproductive — they trigger muscle loss, hormonal disruption, and metabolic adaptation. A moderate deficit of 300–500 calories below TDEE is the evidence-based sweet spot for sustained fat loss without muscle sacrifice."""},

        {"id": "doc_002", "topic": "Macronutrients: Protein, Carbohydrates, and Fats",
         "text": """Macronutrients are the three primary energy-providing nutrients: protein, carbohydrates, and fats.

Protein (4 kcal/g) is essential for muscle repair, immune function, enzyme production, and satiety. Adults should consume 0.8–1.0 g per kg of body weight for general health; those exercising regularly benefit from 1.2–2.0 g/kg. High-protein foods include chicken breast, eggs, lentils, Greek yogurt, tofu, and fish.

Carbohydrates (4 kcal/g) are the body's preferred fuel source. Complex carbs (oats, brown rice, sweet potatoes, legumes) digest slowly and provide sustained energy. Simple sugars cause rapid blood sugar spikes and crashes.

Fats (9 kcal/g) are vital for hormone production, fat-soluble vitamin absorption (A, D, E, K), and cell membrane integrity. Healthy sources include avocado, olive oil, nuts, seeds, and fatty fish. Trans fats should be avoided entirely.

A balanced macronutrient split for general health is roughly 45–65% carbs, 20–35% fat, and 10–35% protein."""},

        {"id": "doc_003", "topic": "Hydration and Water Intake",
         "text": """Water is the most essential nutrient — the body is approximately 60% water, and even mild dehydration (1–2% body weight loss) impairs physical performance, concentration, and mood.

General guidelines recommend 2.7 litres per day for women and 3.7 litres per day for men from all sources combined (food contributes about 20%). Active individuals require significantly more.

A practical check is urine colour: pale yellow indicates good hydration; dark yellow or amber signals a need to drink more.

Sports drinks containing sodium and electrolytes are beneficial during prolonged exercise exceeding 60–90 minutes. For shorter workouts, plain water is sufficient.

Dehydration signs include dry mouth, headache, fatigue, dizziness, and reduced urine output."""},

        {"id": "doc_004", "topic": "Cardiovascular Exercise and Heart Health",
         "text": """Cardiovascular (aerobic) exercise involves sustained movement that raises heart rate and challenges the heart and lungs. Regular cardio strengthens the heart muscle, lowers resting heart rate, reduces blood pressure, improves cholesterol profiles (raises HDL, lowers LDL and triglycerides), and reduces the risk of type 2 diabetes, stroke, and certain cancers.

The World Health Organization (WHO) recommends adults perform at least 150–300 minutes of moderate-intensity aerobic activity or 75–150 minutes of vigorous activity per week.

Moderate intensity corresponds to 50–70% of maximum heart rate (MHR), calculated as 220 minus age. Vigorous intensity is 70–85% MHR.

HIIT (High-Intensity Interval Training) alternates short bursts of maximum effort with recovery periods. It produces similar cardiovascular benefits as steady-state cardio in less time and elevates post-exercise metabolic rate (EPOC)."""},

        {"id": "doc_005", "topic": "Strength Training and Muscle Building",
         "text": """Strength (resistance) training involves working muscles against load. It increases muscle mass, bone density, metabolic rate, functional strength, and insulin sensitivity. The ACSM recommends resistance training at least 2 days per week for all adults.

Key principles include progressive overload (gradually increasing load, reps, or intensity), specificity (training muscles you want to develop), and recovery (muscles grow during rest).

For hypertrophy (muscle growth): 3–5 sets of 8–12 reps at 65–85% of 1RM with 60–90 seconds rest. For strength: 3–6 sets of 1–6 reps at 85–100% 1RM with 2–5 minutes rest.

Beginners should start with compound movements (squats, deadlifts, bench press, rows, overhead press). Protein intake post-workout (within 30–60 minutes) supports muscle protein synthesis."""},

        {"id": "doc_006", "topic": "Sleep and Recovery for Fitness",
         "text": """Sleep is the most underrated performance and weight-management tool. Adults require 7–9 hours per night. Chronic sleep deprivation elevates cortisol (stress hormone), suppresses leptin (satiety hormone), increases ghrelin (hunger hormone), and significantly impairs muscle recovery.

During deep sleep, the pituitary gland releases 70–80% of daily growth hormone, which drives muscle repair and fat metabolism.

Sleep deprivation is directly linked to weight gain: studies show sleep-restricted individuals consume 300–400 more calories per day, primarily from high-fat, high-sugar foods.

Sleep hygiene: maintain a consistent sleep schedule; avoid screens 30–60 minutes before bed (blue light suppresses melatonin); keep bedroom cool (18–20°C is optimal); avoid caffeine after 2 PM."""},

        {"id": "doc_007", "topic": "Healthy Eating Patterns and Meal Timing",
         "text": """Evidence consistently supports eating patterns rich in whole, minimally processed foods. The Mediterranean diet, DASH diet, and plant-forward diets are associated with reduced cardiovascular disease, diabetes, and all-cause mortality.

Common principles: fill half your plate with vegetables and fruit; choose whole grains over refined; include lean proteins; use healthy fats; limit added sugars (< 25g/day for women, < 36g/day for men per AHA); limit sodium (< 2300 mg/day).

Spreading protein across 3–5 meals (25–40g per meal) maximises muscle protein synthesis.

Intermittent fasting (IF) — such as 16:8 — can help some people manage caloric intake but is not superior to continuous caloric restriction when calories are matched.

Eating mindfully — slowly, without distractions, stopping at 80% fullness — reduces overconsumption."""},

        {"id": "doc_008", "topic": "BMI, Body Composition, and Healthy Weight Ranges",
         "text": """Body Mass Index (BMI) is calculated as weight (kg) divided by height (m) squared. WHO categories: Underweight < 18.5; Normal 18.5–24.9; Overweight 25–29.9; Obese Class I 30–34.9; Obese Class II 35–39.9; Obese Class III ≥ 40.

BMI has important limitations: it does not distinguish between fat mass and muscle mass, nor does it reflect fat distribution. Visceral fat (stored around abdominal organs) is more metabolically harmful than subcutaneous fat, even at a normal BMI.

Better metrics include waist circumference (risk increases above 80 cm for women, 94 cm for men), and body fat percentage (healthy ranges: 10–20% for men, 18–28% for women).

A 5–10% reduction in body weight — if overweight — produces clinically significant improvements in blood pressure, blood sugar, and cholesterol."""},

        {"id": "doc_009", "topic": "Stress Management and Mental Wellness in Fitness",
         "text": """Chronic stress chronically elevates cortisol, which promotes fat storage (especially visceral), muscle breakdown, sugar cravings, poor sleep, and immune suppression — all of which undermine fitness goals.

Exercise is one of the most effective stress-reduction strategies: aerobic exercise reduces cortisol post-session, increases endorphins, and reduces symptoms of anxiety and depression comparably to medication in mild-to-moderate cases.

Mindfulness practices — meditation, diaphragmatic breathing, yoga nidra — activate the parasympathetic nervous system. Even 10 minutes of daily meditation reduces perceived stress over 8 weeks.

Set process-based goals ("I will exercise 4 times this week") rather than outcome goals ("I will lose 5 kg") to maintain motivation. Social support increases long-term adherence by 30–50%."""},

        {"id": "doc_010", "topic": "Common Fitness Myths and Misconceptions",
         "text": """Myth 1 — Spot reduction works: Doing crunches does not burn belly fat specifically. Fat loss occurs systemically through overall caloric deficit.

Myth 2 — Cardio is the only way to lose weight: Resistance training builds muscle, which raises resting metabolic rate. A combined approach is superior to either alone.

Myth 3 — Eating fat makes you fat: Excess total calories — from any macronutrient — cause fat storage. Healthy fats are essential and satiating.

Myth 4 — You need supplements to build muscle: Whole-food protein sources are sufficient for most people. Creatine monohydrate is the only supplement with robust evidence for strength and muscle gain.

Myth 5 — More exercise is always better: Overtraining leads to injury, hormonal imbalance, and performance decline.

Myth 6 — Static stretching before exercise prevents injury: Dynamic warm-up is more effective pre-workout; static stretching is better post-workout."""},

        {"id": "doc_011", "topic": "Nutrition for Different Life Stages",
         "text": """Children and adolescents (5–18 years): Higher caloric needs per kg for growth; critical for calcium, iron, and vitamin D. Avoid extreme diets during developmental windows.

Young adults (18–35): Caloric needs stabilise. Muscle-building is easiest due to favourable hormonal environment.

Adults (35–50): Metabolic rate gradually declines (~1–2% per decade from age 30). Maintaining muscle mass through resistance training becomes increasingly important.

Older adults (50+): Protein requirements increase (1.2–1.6 g/kg/day) to combat sarcopenia (age-related muscle loss). Vitamin B12 absorption decreases with age. Weight-bearing exercise and balance training reduce fall risk.

Pregnant women: Caloric surplus of ~300 kcal/day in second and third trimesters. Critical micronutrients: folate, iron, calcium, iodine, omega-3 DHA."""},

        {"id": "doc_012", "topic": "Creating a Sustainable Fitness Routine",
         "text": """Sustainability is the single most important factor in long-term fitness success. The best exercise plan is the one you will actually do consistently over months and years.

Building a sustainable routine: start at a level that is slightly challenging but not overwhelming; schedule workouts like appointments; anchor habits to existing behaviours.

A balanced weekly structure for beginners: 2–3 strength sessions (full body), 2–3 moderate cardio sessions (30 minutes), 1–2 rest or active recovery days. Total: 150+ minutes of moderate activity meeting WHO guidelines.

Aim for 80% adherence (missing 1–2 workouts per week is normal) rather than perfection. Workout partners or group classes improve consistency by 30–50%. A missed session is never a failure — returning is what counts."""},
    ]

    texts      = [d["text"]  for d in DOCUMENTS]
    ids        = [d["id"]    for d in DOCUMENTS]
    metadatas  = [{"topic": d["topic"]} for d in DOCUMENTS]
    embeddings = embedder.encode(texts).tolist()
    collection.add(documents=texts, embeddings=embeddings, ids=ids, metadatas=metadatas)

    # ── State ──────────────────────────────────────────────
    class CapstoneState(TypedDict):
        question:      str
        messages:      List[dict]
        route:         str
        retrieved:     str
        sources:       List[str]
        tool_result:   str
        answer:        str
        faithfulness:  float
        eval_retries:  int
        search_results: str

    # ── Nodes ──────────────────────────────────────────────
    def memory_node(state):
        msgs = state.get("messages", []) + [{"role": "user", "content": state["question"]}]
        return {"messages": msgs[-6:]}

    def router_node(state):
        recent = "; ".join(
            f"{m['role']}: {m['content'][:60]}"
            for m in state.get("messages", [])[-3:-1]
        ) or "none"
        prompt = f"""You are a router for a Health & Fitness Advisor chatbot.

Available options:
- retrieve: search the knowledge base for health/fitness/nutrition questions
- memory_only: answer from conversation history (e.g. 'what did you just say?', 'can you repeat that?')
- tool: use DuckDuckGo web search (e.g. latest fitness research, recent diet trends, breaking health news, current studies)

Recent conversation: {recent}
Current question: {state["question"]}

Reply with ONLY one word: retrieve / memory_only / tool"""
        dec = llm.invoke(prompt).content.strip().lower()
        if "memory" in dec:  dec = "memory_only"
        elif "tool" in dec:  dec = "tool"
        else:                dec = "retrieve"
        return {"route": dec}

    def retrieval_node(state):
        emb     = embedder.encode([state["question"]]).tolist()
        results = collection.query(query_embeddings=emb, n_results=3)
        chunks  = results["documents"][0]
        topics  = [m["topic"] for m in results["metadatas"][0]]
        context = "\n\n---\n\n".join(f"[{topics[i]}]\n{chunks[i]}" for i in range(len(chunks)))
        return {"retrieved": context, "sources": topics}

    def skip_retrieval_node(state):
        return {"retrieved": "", "sources": []}

    def tool_node(state):
        try:
            from ddgs import DDGS
            with DDGS() as ddgs:
                raw = list(ddgs.text(state["question"] + " health fitness", max_results=4))
            tr = "\n\n".join(
                f"Source: {r.get('title','')}\n{r.get('body','')[:300]}"
                for r in raw
            ) if raw else "Web search returned no results."
        except Exception as e:
            tr = f"Web search unavailable: {e}. Relying on knowledge base."
        return {"tool_result": tr, "search_results": tr}

    def answer_node(state):
        ctx_parts = []
        if state.get("retrieved"):   ctx_parts.append(f"KNOWLEDGE BASE:\n{state['retrieved']}")
        if state.get("tool_result"): ctx_parts.append(f"WEB SEARCH RESULTS:\n{state['tool_result']}")
        ctx = "\n\n".join(ctx_parts)

        if ctx:
            sys_prompt = f"""You are FitGuide, a knowledgeable and empathetic Health & Fitness Advisor.
You serve users of all ages with evidence-based, practical guidance on nutrition, exercise, weight management, and wellness.

Answer using ONLY the information provided in the context below.
If the answer is not in the context, say clearly: "I don't have specific information on that in my knowledge base. I recommend consulting a registered dietitian or certified fitness professional for personalised advice."
Do NOT add information from your training data beyond what is in the context.
Keep answers clear, warm, and actionable. Use bullet points where helpful.

{ctx}"""
        else:
            sys_prompt = "You are FitGuide, a Health & Fitness Advisor. Answer warmly based on the conversation history."

        if state.get("eval_retries", 0) > 0:
            sys_prompt += "\n\nIMPORTANT: Your previous answer did not meet quality standards. Answer using ONLY information explicitly stated in the context above."

        from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
        lc_msgs = [SystemMessage(content=sys_prompt)]
        for m in state.get("messages", [])[:-1]:
            lc_msgs.append(HumanMessage(content=m["content"]) if m["role"] == "user"
                           else AIMessage(content=m["content"]))
        lc_msgs.append(HumanMessage(content=state["question"]))
        return {"answer": llm.invoke(lc_msgs).content}

    FAITHFULNESS_THRESHOLD = 0.7
    MAX_EVAL_RETRIES       = 2

    def eval_node(state):
        ctx     = state.get("retrieved", "")[:500]
        retries = state.get("eval_retries", 0)
        if not ctx:
            return {"faithfulness": 1.0, "eval_retries": retries + 1}
        try:
            score = float(llm.invoke(
                f"Rate faithfulness 0.0-1.0. Reply with ONLY a number.\nContext: {ctx}\nAnswer: {state.get('answer','')[:300]}"
            ).content.strip().split()[0].replace(",", "."))
            score = max(0.0, min(1.0, score))
        except:
            score = 0.5
        return {"faithfulness": score, "eval_retries": retries + 1}

    def save_node(state):
        msgs = state.get("messages", []) + [{"role": "assistant", "content": state.get("answer", "")}]
        return {"messages": msgs}

    def route_decision(state):
        r = state.get("route", "retrieve")
        if r == "tool":        return "tool"
        if r == "memory_only": return "skip"
        return "retrieve"

    def eval_decision(state):
        if state.get("faithfulness", 1.0) >= FAITHFULNESS_THRESHOLD or state.get("eval_retries", 0) >= MAX_EVAL_RETRIES:
            return "save"
        return "answer"

    # ── Graph ──────────────────────────────────────────────
    from langgraph.graph import StateGraph, END
    g = StateGraph(CapstoneState)
    for name, fn in [
        ("memory",   memory_node),
        ("router",   router_node),
        ("retrieve", retrieval_node),
        ("skip",     skip_retrieval_node),
        ("tool",     tool_node),
        ("answer",   answer_node),
        ("eval",     eval_node),
        ("save",     save_node),
    ]:
        g.add_node(name, fn)

    g.set_entry_point("memory")
    g.add_edge("memory", "router")
    g.add_conditional_edges("router", route_decision,
                            {"retrieve": "retrieve", "skip": "skip", "tool": "tool"})
    for n in ["retrieve", "skip", "tool"]:
        g.add_edge(n, "answer")
    g.add_edge("answer", "eval")
    g.add_conditional_edges("eval", eval_decision, {"answer": "answer", "save": "save"})
    g.add_edge("save", END)

    from langgraph.checkpoint.memory import MemorySaver
    agent_app = g.compile(checkpointer=MemorySaver())
    return agent_app, collection


# ── Session state ─────────────────────────────────────────
if "messages"    not in st.session_state: st.session_state.messages    = []
if "thread_id"   not in st.session_state: st.session_state.thread_id   = str(uuid.uuid4())[:8]
if "total_asked" not in st.session_state: st.session_state.total_asked = 0
if "agent_ready" not in st.session_state: st.session_state.agent_ready = False

# ── Load agent ────────────────────────────────────────────
try:
    agent_app, collection = load_agent()
    st.session_state.agent_ready = True
except Exception as e:
    st.error(f"❌ Failed to load agent: {e}")
    st.stop()

KB_TOPICS = [
    "Caloric Balance & Weight Management",
    "Macronutrients: Protein, Carbs & Fats",
    "Hydration & Water Intake",
    "Cardiovascular Exercise & Heart Health",
    "Strength Training & Muscle Building",
    "Sleep & Recovery for Fitness",
    "Healthy Eating Patterns & Meal Timing",
    "BMI, Body Composition & Weight Ranges",
    "Stress Management & Mental Wellness",
    "Common Fitness Myths & Misconceptions",
    "Nutrition for Different Life Stages",
    "Creating a Sustainable Fitness Routine",
]

ROUTE_ICONS = {"retrieve": "📚", "tool": "🌐", "memory_only": "💭", "?": "⚙️"}

SUGGESTIONS = [
    "How much protein do I need daily?",
    "Best exercises for beginners?",
    "How to lose weight safely?",
    "How much water should I drink?",
    "Is 7 hours of sleep enough?",
]

# ── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 8px 0 16px 0;'>
        <div style='font-family: "DM Serif Display", serif; font-size: 1.5rem; color: #E8F5EC; line-height: 1.1;'>
            💪 FitGuide
        </div>
        <div style='font-size: 0.78rem; color: rgba(255,255,255,0.55); margin-top: 4px;'>
            AI Health & Fitness Advisor
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Session</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style='background: rgba(255,255,255,0.08); border-radius: 10px; padding: 10px 14px; margin-bottom: 12px;'>
        <div style='font-size: 0.75rem; color: rgba(255,255,255,0.5); margin-bottom: 4px;'>Session ID</div>
        <div style='font-family: monospace; font-size: 0.88rem; color: #E9C46A;'>{st.session_state.thread_id}</div>
    </div>
    <div style='display: flex; gap: 8px; margin-bottom: 12px;'>
        <div style='flex: 1; background: rgba(255,255,255,0.08); border-radius: 10px; padding: 10px; text-align: center;'>
            <div style='font-size: 1.4rem; font-weight: 600; color: #E9C46A;'>{st.session_state.total_asked}</div>
            <div style='font-size: 0.7rem; color: rgba(255,255,255,0.5);'>Questions</div>
        </div>
        <div style='flex: 1; background: rgba(255,255,255,0.08); border-radius: 10px; padding: 10px; text-align: center;'>
            <div style='font-size: 1.4rem; font-weight: 600; color: #74C69D;'>12</div>
            <div style='font-size: 0.7rem; color: rgba(255,255,255,0.5);'>Docs in KB</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🗑️  New Conversation", use_container_width=True):
        st.session_state.messages    = []
        st.session_state.thread_id   = str(uuid.uuid4())[:8]
        st.session_state.total_asked = 0
        st.rerun()

    st.markdown('<div class="section-label" style="margin-top:20px;">Knowledge Base</div>', unsafe_allow_html=True)
    for t in KB_TOPICS:
        st.markdown(f'<span class="topic-pill">• {t}</span>', unsafe_allow_html=True)

    st.markdown('<div class="section-label" style="margin-top:20px;">Powered By</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size: 0.75rem; color: rgba(255,255,255,0.45); line-height: 1.8;'>
        🦙 Llama 3.3 70B (Groq)<br>
        🔗 LangGraph StateGraph<br>
        🗄️ ChromaDB + all-MiniLM-L6<br>
        🦆 DuckDuckGo Web Search<br>
        ✅ Self-reflection Eval Loop
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="margin-top:24px; font-size: 0.68rem; color: rgba(255,255,255,0.25); text-align: center;">Debdyuti Chakraborty · 23051339<br>Agentic AI Hands-On Course</div>', unsafe_allow_html=True)


# ── Main content ──────────────────────────────────────────
# Header
st.markdown("""
<div class="fitguide-header">
    <h1 class="fitguide-title">Fit<span>Guide</span> 💪</h1>
    <p class="fitguide-subtitle">Evidence-based Health & Fitness Advisor — powered by RAG + Web Search + Self-Reflection</p>
</div>
""", unsafe_allow_html=True)

# Stats bar
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="stat-chip"><span class="dot"></span>Agent Online</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="stat-chip">📚 12 KB Documents</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="stat-chip">🌐 Live Web Search</div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="stat-chip">🧠 Conversation Memory</div>', unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)

# Welcome card (shown when no messages yet)
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-card">
        <h3>👋 Welcome to FitGuide</h3>
        <p style="margin: 0 0 4px 0; font-size: 0.92rem;">
            Ask me anything about nutrition, exercise, weight management, sleep, hydration, or general wellness.
            I'll give you evidence-based answers — and search the web for the latest research when needed.
        </p>
        <div class="suggestion-row">
            <span class="suggestion">💧 Daily water intake?</span>
            <span class="suggestion">🏋️ Protein for muscle gain?</span>
            <span class="suggestion">⚖️ Safe weight loss rate?</span>
            <span class="suggestion">😴 Sleep & fitness recovery?</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='margin: 16px 0;'></div>", unsafe_allow_html=True)

# Chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="🧑"):
            st.write(msg["content"])
    else:
        with st.chat_message("assistant", avatar="💪"):
            st.write(msg["content"])
            if msg.get("meta"):
                meta = msg["meta"]
                route      = meta.get("route", "?")
                faith      = meta.get("faith", 0.0)
                sources    = meta.get("sources", [])
                route_icon = ROUTE_ICONS.get(route, "⚙️")
                route_cls  = f"route-{route.replace('_','-')}" if route in ["retrieve","tool"] else "route-memory"
                src_str    = " · ".join(sources[:2]) if sources else "—"
                st.markdown(f"""
                <div class="meta-badge">
                    {route_icon} <b>{route}</b>
                    &nbsp;·&nbsp; 🎯 Faithfulness: {faith:.2f}
                    &nbsp;·&nbsp; 📌 {src_str}
                </div>
                """, unsafe_allow_html=True)

# Chat input
prompt = st.chat_input("Ask FitGuide about nutrition, exercise, weight loss, sleep...")

if prompt:
    # Show user message immediately
    with st.chat_message("user", avatar="🧑"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.total_asked += 1

    # Run agent
    with st.chat_message("assistant", avatar="💪"):
        with st.spinner("FitGuide is thinking..."):
            try:
                config = {"configurable": {"thread_id": st.session_state.thread_id}}
                result = agent_app.invoke({"question": prompt}, config=config)
                answer  = result.get("answer", "Sorry, I couldn't generate an answer. Please try again.")
                faith   = result.get("faithfulness", 0.0)
                route   = result.get("route", "?")
                sources = result.get("sources", [])
            except Exception as e:
                answer  = f"⚠️ An error occurred: {str(e)}"
                faith, route, sources = 0.0, "?", []

        st.write(answer)
        route_icon = ROUTE_ICONS.get(route, "⚙️")
        src_str    = " · ".join(sources[:2]) if sources else "—"
        st.markdown(f"""
        <div class="meta-badge">
            {route_icon} <b>{route}</b>
            &nbsp;·&nbsp; 🎯 Faithfulness: {faith:.2f}
            &nbsp;·&nbsp; 📌 {src_str}
        </div>
        """, unsafe_allow_html=True)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "meta": {"route": route, "faith": faith, "sources": sources}
    })
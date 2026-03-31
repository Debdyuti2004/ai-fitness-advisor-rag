# 💪 FitGuide — AI Health & Fitness Advisor

FitGuide is an intelligent AI-powered assistant that provides evidence-based guidance on fitness, nutrition, and wellness.

Built using **LangGraph**, **Retrieval-Augmented Generation (RAG)**, and **real-time web search**, it combines structured knowledge with dynamic reasoning to deliver high-quality answers.

---

## 🚀 Features

- 📚 **Knowledge Base (RAG)** using ChromaDB  
- 🌐 **Real-time Web Search** (DuckDuckGo)  
- 🧠 **Conversation Memory** (LangGraph state)  
- 🔀 **Intelligent Routing**
  - Retrieval (KB)
  - Tool (web search)
  - Memory  
- ✅ **Self-Evaluation Loop** (answer quality check)  
- 💬 **Interactive UI** built with Streamlit  

---

## 🛠️ Tech Stack

- **LLM:** Groq (Llama 3.3 70B)  
- **Framework:** LangGraph  
- **Vector DB:** ChromaDB  
- **Embeddings:** SentenceTransformers (all-MiniLM-L6-v2)  
- **Frontend:** Streamlit  
- **Search:** DuckDuckGo  

---

## ⚙️ Installation

### 1️⃣ Clone the repository
bash:
git clone https://github.com/your-username/fitguide-ai-agent.git
cd fitguide-ai-agent

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Setup environment variables
Create a .env file:
GROQ_API_KEY=your_api_key_here

▶️ Run the App
streamlit run capstone_streamlit.py
Then open:
http://localhost:8501
🧠 How It Works
User enters a query
Agent routes the query:
📚 Knowledge Base
🌐 Web Search
💭 Memory
Relevant context is retrieved
LLM generates answer
Evaluation loop checks answer quality
Final response is displayed

📂 Project Structure
.
├── capstone_streamlit.py   # Main Streamlit app
├── Capstone_project_23051339_Debdyuti.ipynb  # Development notebook
├── requirements.txt
├── .env.example
└── README.md

🎯 Example Queries
How can I lose weight safely?
How much protein do I need daily?
What is a balanced diet?
Latest fitness research trends
How does sleep affect muscle growth?

⚠️ Disclaimer
This application provides general health and fitness guidance.
It is not a substitute for professional medical advice.
Consult a qualified healthcare provider for personalized recommendations.

👨‍💻 Author
Debdyuti Chakraborty
BTech CSE | AI & ML Enthusiast

⭐ If you like this project

Give it a star ⭐ and feel free to contribute!

📜 License
This project is licensed under the Apache License 2.0.

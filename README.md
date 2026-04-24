# 🇮🇳 Indian Retail GenAI Support System

## 🚀 Overview

A GenAI-based customer support chatbot for Indian retail platforms — built with **LangChain** and **LangGraph**. Supports Hinglish queries and handles order tracking, FAQs, complaints, and pricing.

---

## 📁 Project Structure

```
retail-genai-langgraph/
├── streamlit_app.py              # Streamlit UI entry point
├── requirements.txt
├── .env.example
└── app/
    ├── __init__.py
    └── graph/
        ├── __init__.py
        ├── retail_graph.py       # LangGraph graph definition
        └── tools/
            ├── __init__.py
            ├── pricing_tool.py   # Price optimization
            ├── order_tool.py     # Order tracking
            ├── faq_tool.py       # FAQ responses
            └── complaint_tool.py # Complaint registration
```

---

## 💡 Features

- 📦 **Order Tracking** — Track order by ID
- ❓ **FAQ Responses** — Return, refund, cancel, payment policies
- 🎫 **Complaint Handling** — Auto ticket generation
- 💰 **Pricing Info** — Category-based discount logic
- 🤖 **General Queries** — LLM fallback (GPT-3.5)
- 🙏 **Hinglish Support** — Understands mixed Hindi-English queries

---

## 🧠 Architecture

```
User Query
    │
    ▼
classify_intent (keyword-based router)
    │
    ├── order      → handle_order      (track_order)
    ├── pricing    → handle_pricing    (optimize_price)
    ├── complaint  → handle_complaint  (register_complaint)
    ├── faq        → handle_faq        (get_faq_answer)
    └── general    → handle_general    (LLM via ChatOpenAI)
```

---

## ⚙️ Setup

### 1. Clone and install

```bash
git clone https://github.com/your-repo/retail-genai-langgraph.git
cd retail-genai-langgraph
pip install -r requirements.txt
```

### 2. Set your API key

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 3. Run locally

```bash
streamlit run streamlit_app.py
```

---

## ☁️ Deploy on Streamlit Cloud

1. Push the repo to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud) → New App
3. Set `streamlit_app.py` as the entry point
4. Add `OPENAI_API_KEY` in **Secrets** (Settings → Secrets)

```toml
OPENAI_API_KEY = "sk-..."
```

---

## 🐛 Common Errors Fixed

| Error | Fix Applied |
|---|---|
| `ModuleNotFoundError: from graph.tools.pricing_tool` | Changed to `from app.graph.tools.pricing_tool` |
| Missing `__init__.py` | Added to `app/`, `app/graph/`, `app/graph/tools/` |
| `langchain_openai` not in requirements | Added `langchain-openai` to `requirements.txt` |

---

## 📌 Future Scope

- [ ] Add RAG (document-based answers)
- [ ] Add CrewAI agents
- [ ] Add real order/product API integration
- [ ] Multilingual support (Tamil, Telugu, Bengali)

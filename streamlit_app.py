import streamlit as st
import os
from langgraph.graph import StateGraph
from langchain.chat_models import ChatOpenAI

# 🔐 API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    temperature=0.7,
    openai_api_key=OPENAI_API_KEY
)

class State(dict):
    pass

# 🔹 Intent Classification
def classify(state):
    query = state["query"].lower()

    if "order" in query or "kab" in query:
        state["intent"] = "ORDER"
    elif "refund" in query or "return" in query:
        state["intent"] = "FAQ"
    elif "problem" in query or "complaint" in query:
        state["intent"] = "COMPLAINT"
    else:
        state["intent"] = "GENERAL"

    return state

# 🔹 Nodes
def faq_node(state):
    state["response"] = "Return policy is 7 days. Refund in 5-7 days."
    return state

def order_node(state):
    state["response"] = "Aapka order kal deliver ho jayega 🚚"
    return state

def complaint_node(state):
    state["response"] = "Complaint registered. Our team will contact you."
    return state

def general_node(state):
    response = llm.invoke(state["query"])
    state["response"] = response.content
    return state

# 🔹 Graph
graph = StateGraph(State)

graph.add_node("classify", classify)
graph.add_node("faq", faq_node)
graph.add_node("order", order_node)
graph.add_node("complaint", complaint_node)
graph.add_node("general", general_node)

graph.set_entry_point("classify")

graph.add_conditional_edges(
    "classify",
    lambda s: s["intent"],
    {
        "FAQ": "faq",
        "ORDER": "order",
        "COMPLAINT": "complaint",
        "GENERAL": "general"
    }
)

graph.set_finish_point("faq")
graph.set_finish_point("order")
graph.set_finish_point("complaint")
graph.set_finish_point("general")

app = graph.compile()

# 🌐 UI
st.set_page_config(page_title="Retail GenAI", page_icon="🛍️")
st.title("🇮🇳 Indian Retail GenAI Support System")

if "chat" not in st.session_state:
    st.session_state.chat = []

query = st.text_input("Ask your question:")

if query:
    result = app.invoke({"query": query})
    answer = result["response"]

    st.session_state.chat.append(("You", query))
    st.session_state.chat.append(("AI", answer))

for sender, message in st.session_state.chat:
    if sender == "You":
        st.markdown(f"**🧑 You:** {message}")
    else:
        st.markdown(f"**🤖 AI:** {message}")

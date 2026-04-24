import streamlit as st
from langgraph.graph import StateGraph
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI()

class State(dict):
    pass

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

def faq_node(state):
    state["response"] = "Return policy is 7 days. Refund in 5-7 days."
    return state

def order_node(state):
    state["response"] = "Aapka order kal deliver ho jayega 🚚"
    return state

def complaint_node(state):
    state["response"] = "Complaint register ho gayi hai."
    return state

def general_node(state):
    state["response"] = llm.predict(state["query"])
    return state

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

# 🌐 Streamlit UI
st.title("🇮🇳 Indian Retail GenAI Support System")

query = st.text_input("Ask your question:")

if query:
    result = app.invoke({"query": query})
    st.write(result["response"])

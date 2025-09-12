import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage

# Load API key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Configure Groq model
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    temperature=0.7
)

# Page config
st.set_page_config(page_title="SmartRent", layout="wide")

st.title("💬 SmartBot Assistant")
st.write("Ask anything about rental listings, pricing trends, or platform features.")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input box at bottom
user_input = st.chat_input("Type your message and press Enter")

# Process input before rendering chat
if user_input:
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    bot_reply = llm.invoke(st.session_state.chat_history)
    st.session_state.chat_history.append(bot_reply)
    

# Display chat messages after input is processed
for msg in st.session_state.chat_history:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(msg.content)
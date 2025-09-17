import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from streamlit_mic_recorder import speech_to_text

# Load API key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    temperature=0.7
)

st.set_page_config(page_title="SmartRent", layout="wide")
st.title("💬 SmartBot Assistant")
col1,col2 = st.columns(spec = [0.8,0.2],vertical_alignment='center')
with col1:
    st.write("Ask anything about rental listings, pricing trends, or platform features.")
with col2:
    mic_text = speech_to_text(
        language='en',
        start_prompt="🎤 Start Recording",
        stop_prompt="⏹️ Stop Recording",
        just_once=True,
        key="mic_button"
    )

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    with st.chat_message("user" if isinstance(msg, HumanMessage) else "assistant"):
        st.markdown(msg.content)

user_input = st.chat_input("Type your message and press Enter")

if user_input:
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    bot_reply = llm.invoke(st.session_state.chat_history)
    st.session_state.chat_history.append(bot_reply)
    st.rerun()

if mic_text:
    st.session_state.chat_history.append(HumanMessage(content=mic_text))
    bot_reply = llm.invoke(st.session_state.chat_history)
    st.session_state.chat_history.append(bot_reply)
    st.rerun()
import streamlit as st
import datetime
import requests

BASE_URL = "http://localhost:8000"

# Page Config
st.set_page_config(
    page_title="EaseTrip",
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    /* 2. Background color → Baby Pink */
    [data-testid="stAppViewContainer"] {
        background: #D6F5D6!important;  /* light greenish */
    }

    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }

    /* 1. Q&A boxes full width */
    .user-msg, .ai-msg {
        background-color: #F5F5F5;
        padding: 15px 20px;
        border-radius: 12px;
        margin: 10px 0;
        max-width: 100% !important;   /* full width */
        text-align: left;
        box-sizing: border-box;
        display: block;
    }

    .user-msg {
        background-color: #B8E6B8;
    }

    .ai-msg {
        background-color: #F0F0F0;
    }

    .timestamp {
        font-size: 0.7em;
        color: #666;
    }

    h1, h3, .stMarkdown, .stChatMessage, .stText {
        color: black !important;  /* 3. Text color black */
    }

    /* 4. User input box full width */
    [data-testid="stChatInput"] {
        width: 100% !important;
        margin: 0 auto !important;
        display: block !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🌍 Welcome to EaseTrip!")
st.markdown("### Plan your dream trip effortlessly with your go to travel buddy!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat Input
user_input = st.chat_input("Where do you want to go and for how long?")

if user_input:
    with st.spinner("Planning your trip..."):
        payload = {"question": user_input}
        response = requests.post(f"{BASE_URL}/query", json=payload)

    # Add user message
    st.session_state.messages.append(("user", user_input, datetime.datetime.now()))

    # Add AI response
    if response.status_code == 200:
        answer = response.json().get("answer", "No answer returned.")
        st.session_state.messages.append(("ai", answer, datetime.datetime.now()))
    else:
        st.session_state.messages.append(("ai", "Bot failed to respond.", datetime.datetime.now()))

# Display Chat
for sender, message, timestamp in st.session_state.messages:
    if sender == "user":
        st.markdown(f"<div class='user-msg'>{message}<div class='timestamp'>{timestamp.strftime('%H:%M')}</div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='ai-msg'>{message}<div class='timestamp'>{timestamp.strftime('%H:%M')}</div></div>", unsafe_allow_html=True)





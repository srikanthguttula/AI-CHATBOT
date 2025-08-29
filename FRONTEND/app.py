import streamlit as st
import requests

# ================== CONFIG ==================
API_BASE = "https://ai-chatbot-42pn.onrender.com"   # Change this if deployed
CHAT_ENDPOINT = f"{API_BASE}/chat"
HEALTH_ENDPOINT = f"{API_BASE}/health"

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ================== SIDEBAR ==================
st.sidebar.title("⚙️ Settings")

# Persona selector
persona = st.sidebar.selectbox(
    "Choose Persona",
    ["Default", "Tutor", "Therapist", "Assistant", "Friend"],
    index=0
)

# Clear chat button
if st.sidebar.button("🧹 Clear Chat"):
    st.session_state["history"] = []
    st.session_state["messages"] = []

# ================== SESSION STATE ==================
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "history" not in st.session_state:
    st.session_state["history"] = []

# ================== HEADER ==================
st.markdown(
    """
    <h1 style='text-align: center; color: #4CAF50;'>🤖 AI Chatbot</h1>
    <p style='text-align: center;'>Talk to your AI assistant with style!</p>
    """,
    unsafe_allow_html=True,
)

# ================== CHAT DISPLAY ==================
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    else:
        st.chat_message("assistant").markdown(msg["content"])

# ================== USER INPUT ==================
if prompt := st.chat_input("Type your message..."):
    # Display user message immediately
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Prepare payload for API
    payload = {
        "message": prompt,
        "persona": None if persona == "Default" else persona,
        "history": st.session_state.history,
    }

    try:
        response = requests.post(CHAT_ENDPOINT, json=payload)
        response.raise_for_status()
        data = response.json()

        bot_reply = data["response"]

        # Display bot reply
        st.chat_message("assistant").markdown(bot_reply)

        # Save to session
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        st.session_state.history.append({"user": prompt, "assistant": bot_reply})

    except Exception as e:
        st.error(f"⚠️ Error: {e}")

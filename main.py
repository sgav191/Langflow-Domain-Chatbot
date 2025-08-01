import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("LANGFLOW_API_KEY", st.secrets.get("LANGFLOW_API_KEY", ""))

if not api_key:
    st.error("❌ LANGFLOW_API_KEY not found.")
    st.stop()

# Langflow API endpoint
url = "https://langflow-ai-3zj2x.ondigitalocean.app/api/v1/run/177d208c-0608-4386-bc35-2e79ac3f46c7"

# Streamlit page config
st.set_page_config(page_title="<< Chat with domAIn >>", layout="centered")

# CSS: Hide top bar, footer, watermark; center layout
st.markdown("""
    <style>
    /* Hide Streamlit branding */
    #MainMenu, footer, header {visibility: hidden;}

    /* Center content */
    .st-emotion-cache-1y4p8pa { justify-content: center; }

    /* Clean input box and message spacing */
    .block-container { padding-top: 2rem; }
    .stChatMessage { margin-bottom: 1.5rem; }

    /* Try to obscure the watermark (white overlay hack) */
    [data-testid="stAppViewContainer"]::after {
        content: "";
        position: fixed;
        bottom: 10px;
        right: 10px;
        width: 180px;
        height: 30px;
        background: white;
        z-index: 9999;
        pointer-events: none;
    }
    </style>
""", unsafe_allow_html=True)

# Centered title and description
st.markdown("<h1 style='text-align: center;'>&lt;&lt; Chat with domAIn &gt;&gt;</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>&lt;&lt; Ask me anything &gt;&gt;</p>", unsafe_allow_html=True)

# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="human avatar.jpg"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant", avatar="AI avatar.jpg"):
            st.markdown(msg["content"])

# Handle user input
if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="human avatar.jpg"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="AI avatar.jpg"):
        with st.spinner("Thinking..."):
            try:
                payload = {
                    "output_type": "chat",
                    "input_type": "chat",
                    "input_value": prompt
                }
                headers = {
                    "Content-Type": "application/json",
                    "x-api-key": api_key
                }
                response = requests.post(url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                message = data["outputs"][0]["outputs"][0]["results"]["message"]["text"]
            except Exception as e:
                message = f"Error: {e}"

            st.markdown(message)
            st.session_state.messages.append({"role": "assistant", "content": message})

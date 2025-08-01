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

# Streamlit config
st.set_page_config(page_title="<< Chat with domAIn >>", layout="centered")

# Inject CSS to remove top bar, watermark, and center layout
st.markdown("""
    <style>
    /* Hide Streamlit top bar */
    header[data-testid="stHeader"] {
        visibility: hidden !important;
        height: 0px !important;
        position: absolute !important;
        top: -100px;
    }

    /* Hide all watermark/branding decorations */
    #MainMenu, footer, [data-testid="stDecoration"], .viewerBadge_container__1QSob {
        visibility: hidden !important;
        display: none !important;
        height: 0px !important;
    }

    /* Layout refinements */
    .block-container {
        padding-top: 2rem;
    }
    .stChatMessage {
        margin-bottom: 1.5rem;
    }
    .st-emotion-cache-1y4p8pa {
        justify-content: center;
    }
    html, body {
        margin-top: 0 !important;
        padding-top: 0 !important;
        background-color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Centered title and description
st.markdown("<h1 style='text-align: center;'>&lt;&lt;Chat with domAIn&gt;&gt;</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>&lt;&lt; Ask me anything &gt;&gt;</p>", unsafe_allow_html=True)

# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="human avatar.jpg"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant", avatar="AI avatar.jpg"):
            st.markdown(msg["content"])

# Handle user prompt
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

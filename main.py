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

# Inject CSS and JS to hide watermarks and style layout
st.markdown("""
    <style>
    header[data-testid="stHeader"] {
        background: none !important;
    }
    #MainMenu, footer {
        visibility: hidden !important;
        display: none !important;
    }
    .viewerBadge_container__1QSob,
    .viewerBadge_link__qRIco {
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
    }
    .block-container {
        padding-top: 2rem;
    }
    .stChatMessage {
        margin-bottom: 1.5rem;
    }
    .st-emotion-cache-1y4p8pa {
        justify-content: center;
    }
    h1, h2, h3, .stMarkdown {
        text-align: center;
    }
    </style>

    <script>
    setTimeout(function() {
        const badge = window.parent.document.querySelector('.viewerBadge_container__1QSob');
        if (badge) { badge.style.display = 'none'; }
    }, 1000);
    </script>
""", unsafe_allow_html=True)

# Centered title and description
st.markdown("<h1 style='text-align: center;'>&lt;&lt;Chat with domAIn&gt;&gt;</h1>", unsafe_allow_html=True)
st.markdown("<< Ask me anything >>")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
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

import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load env vars locally or from Streamlit secrets
load_dotenv()
api_key = os.getenv("LANGFLOW_API_KEY", st.secrets.get("LANGFLOW_API_KEY", ""))

if not api_key:
	st.error("❌ LANGFLOW_API_KEY not found.")
	st.stop()

# Langflow API endpoint
url = "https://langflow-ai-3zj2x.ondigitalocean.app/api/v1/run/177d208c-0608-4386-bc35-2e79ac3f46c7"

# Streamlit setup
st.set_page_config(page_title="<<domAIn chatbot>>", layout="centered")

# --- CSS Styling ---
st.markdown("""
	<style>
	div[data-baseweb="input"] {
		border: 2px solid #999999 !important;
		border-radius: 12px !important;
		padding: 0.5rem !important;
		background-color: #f9f9f9 !important;
	}
	div[data-baseweb="input"] > div {
		background-color: transparent !important;
		border: none !important;
		padding: 0 !important;
		box-shadow: none !important;
	}
	input {
		background-color: transparent !important;
		color: #333333 !important;
		font-size: 16px !important;
		outline: none !important;
		border: none !important;
		box-shadow: none !important;
	}
	div[data-baseweb="input"]:focus-within {
		border: 2px solid #666666 !important;
	}
	</style>
""", unsafe_allow_html=True)

# Title & prompt
st.title("<<domAIn chatbot>>")
st.markdown("Ask the domAIn Chatbot anything about the book")

# --- Session state setup ---
if "messages" not in st.session_state:
	st.session_state.messages = []

if "user_input" not in st.session_state:
	st.session_state.user_input = ""

# Display chat history
for msg in st.session_state.messages:
	sender = "You" if msg["role"] == "user" else "Chatbot"
	st.markdown(f"**{sender}:** {msg['content']}")

# Input field with memory
user_input = st.text_input("You:", placeholder="Ask a question...", key="user_input")

# If there's input, send it once and reset
if user_input.strip():
	st.session_state.messages.append({"role": "user", "content": user_input})
	st.session_state.user_input = ""  # clear after sending to prevent loops

	with st.spinner("Thinking..."):
		payload = {
			"output_type": "chat",
			"input_type": "chat",
			"input_value": user_input
		}
		headers = {
			"Content-Type": "application/json",
			"x-api-key": api_key
		}

		try:
			response = requests.post(url, json=payload, headers=headers)
			response.raise_for_status()
			data = response.json()
			bot_reply = data["outputs"][0]["outputs"][0]["results"]["message"]["text"]
			st.session_state.messages.append({"role": "bot", "content": bot_reply})
			st.rerun()

		except Exception as e:
			st.session_state.messages.append({"role": "bot", "content": f"Error: {e}"})
			st.rerun()

# Clear chat button
if st.button("Clear chat"):
	st.session_state.messages = []
	st.session_state.user_input = ""
	st.rerun()

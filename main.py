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

# Streamlit setup
st.set_page_config(page_title="<<domAIn chatbot>>", layout="centered")

# --- Custom Font, Styling, and Watermark Removal ---
st.markdown("""
	<style>
	@import url('https://fonts.googleapis.com/css2?family=Inter&display=swap');

	html, body, [class^="css"] *, .stApp, .stMarkdown, .stTextInput input {
		font-family: 'Inter', sans-serif !important;
	}

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

	#MainMenu {visibility: hidden;}
	footer {visibility: hidden;}
	header {visibility: hidden;}
	</style>
""", unsafe_allow_html=True)

# Title and description
st.title("<<domAIn chatbot>>")
st.markdown("Ask the domAIn Chatbot anything about the book")

# Initialize chat history
if "messages" not in st.session_state:
	st.session_state.messages = []

# Initialize control flags
if "just_sent" not in st.session_state:
	st.session_state.just_sent = False
if "clear_input" not in st.session_state:
	st.session_state.clear_input = False

# Handle input clearing
if st.session_state.clear_input:
	st.session_state.clear_input = False
	st.session_state.pop("user_input", None)
	st.rerun()

# Show chat history
for msg in st.session_state.messages:
	sender = "You" if msg["role"] == "user" else "Chatbot"
	st.markdown(f"**{sender}:** {msg['content']}")

# Input field
user_input = st.text_input("You:", placeholder="Ask a question...", key="user_input")

# Handle user input
if user_input and not st.session_state.just_sent:
	st.session_state.messages.append({"role": "user", "content": user_input})
	st.session_state.just_sent = True

	# Call Langflow API
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
		except Exception as e:
			st.session_state.messages.append({"role": "bot", "content": f"Error: {e}"})

	# Prepare input clear for next run
	st.session_state.clear_input = True
	st.rerun()

# Reset send flag
if st.session_state.just_sent:
	st.session_state.just_sent = False

# Optional: clear history
if st.button("Clear chat"):
	st.session_state.messages = []
	st.session_state.clear_input = True
	st.rerun()

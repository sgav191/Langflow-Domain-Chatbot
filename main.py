import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables (for local dev)
load_dotenv()

# Get API key from environment or Streamlit secrets
api_key = os.getenv("LANGFLOW_API_KEY", st.secrets.get("LANGFLOW_API_KEY", ""))
if not api_key:
	st.error("❌ LANGFLOW_API_KEY not found.")
	st.stop()

# Langflow API endpoint
url = "https://langflow-ai-3zj2x.ondigitalocean.app/api/v1/run/177d208c-0608-4386-bc35-2e79ac3f46c7"

# Streamlit layout
st.set_page_config(page_title="<<domAIn chatbot>>", layout="centered")

# ✅ Actual working CSS (thanks to the Streamlit forum thread!)
st.markdown("""
	<style>
	div[data-baseweb="input"] {
		border: 2px solid #999999 !important;
		border-radius: 12px !important;
		padding: 8px !important;
		background-color: #f9f9f9 !important;
	}

	div[data-baseweb="input"]:focus-within {
		border: 2px solid #666666 !important;
		outline: none !important;
		box-shadow: none !important;
	}
	</style>
""", unsafe_allow_html=True)

# App title and instructions
st.title("<<domAIn chatbot>>")
st.markdown("Ask the domAIn Chatbot anything about the book")

# ✅ Label hidden to suppress native focus outlines
user_input = st.text_input(
	label="", 
	placeholder="Ask a question...", 
	label_visibility="collapsed"
)

# Send button logic
if st.button("Send"):
	if not user_input.strip():
		st.warning("Please enter a message.")
	else:
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
				message = data["outputs"][0]["outputs"][0]["results"]["message"]["text"]
				st.markdown(f"**Chatbot says:** {message}")
			except Exception as e:
				st.error(f"Error: {e}")

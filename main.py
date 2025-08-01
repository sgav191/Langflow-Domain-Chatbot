import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables (for local development)
load_dotenv()

# Get API key from environment or Streamlit secrets
api_key = os.getenv("LANGFLOW_API_KEY", st.secrets.get("LANGFLOW_API_KEY", ""))

if not api_key:
	st.error("❌ LANGFLOW_API_KEY not found. Please set it in .env or Streamlit secrets.")
	st.stop()

# Langflow API endpoint
url = "https://langflow-ai-3zj2x.ondigitalocean.app/api/v1/run/177d208c-0608-4386-bc35-2e79ac3f46c7"

# Page settings
st.set_page_config(page_title="<<domAIn chatbot>>", layout="centered")

# Inject custom CSS to style the input box with no red outlines
st.markdown("""
	<style>
	input[type="text"] {
		border: 2px solid #999999 !important;
		border-radius: 12px !important;
		padding: 10px !important;
		outline: none !important;
		box-shadow: none !important;
		background-color: #f9f9f9 !important;
		color: #333333 !important;
		font-size: 16px !important;
	}

	input[type="text"]:focus {
		border: 2px solid #666666 !important;
		box-shadow: none !important;
		outline: none !important;
	}

	input:invalid,
	input[aria-invalid="true"] {
		border-color: #999999 !important;
		box-shadow: none !important;
		outline: none !important;
	}
	</style>
""", unsafe_allow_html=True)

# UI: Title and subtitle
st.title("<<domAIn chatbot>>")
st.markdown("Ask the domAIn Chatbot anything about the book")

# ✅ CUSTOM INPUT (label hidden to suppress accessibility outlines)
user_input = st.text_input(
	label="",
	placeholder="Ask a question...",
	label_visibility="collapsed"
)

# Send button
if st.button("Send"):
	if not user_input.strip():
		st.warning("Please enter a message.")
	else:
		with st.spinner("Thinking..."):
			# Build request payload
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

				# Parse response
				data = response.json()
				message = data["outputs"][0]["outputs"][0]["results"]["message"]["text"]

				# Display chatbot reply
				st.markdown(f"**Chatbot says:** {message}")

			except Exception as e:
				st.error(f"Error: {e}")

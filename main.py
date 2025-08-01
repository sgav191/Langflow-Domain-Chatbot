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

# --- Streamlit App Layout ---
st.set_page_config(page_title="<<domAIn chatbot>>", layout="centered")

# Inject hardcore CSS + JS to override red border styling
st.markdown("""
	<style>
	input[type="text"] {
		border: 2px solid #999999 !important;
		border-radius: 12px !important;
		padding: 8px !important;
		outline: none !important;
		box-shadow: none !important;
		background-color: #f9f9f9 !important;
		color: #333333 !important;
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

	<script>
	const fixTextbox = () => {
		const input = window.parent.document.querySelector('input[type="text"]');
		if (input) {
			input.style.border = "2px solid #999999";
			input.style.borderRadius = "12px";
			input.style.outline = "none";
			input.style.boxShadow = "none";
			input.style.backgroundColor = "#f9f9f9";
			input.style.color = "#333333";
		}
	};
	window.addEventListener("load", fixTextbox);
	</script>
""", unsafe_allow_html=True)

# --- UI ---
st.title("<<domAIn chatbot>>")
st.markdown("Ask the domAIn Chatbot anything about the book")

# User input field
user_input = st.text_input("You:", placeholder="Ask a question...")

# Submit button
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

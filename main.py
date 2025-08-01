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

# Inject CSS to remove red outline and apply grey styling
st.markdown("""
	<style>
	/* Core styling for input box */
	input[type="text"] {
		border: 2px solid #999999 !important;
		border-radius: 12px !important;
		padding: 8px !important;
		outline: none !important;
		box-shadow: none !important;
		background-color: #f9f9f9 !important;
		color: #333333 !important;
	}

	/* On focus (when typing) */
	input[type="text"]:focus {
		border: 2px solid #666666 !important;
		outline: none !important;
		box-shadow: none !important;
	}

	/* Remove red validation borders */
	input:invalid,
	input[aria-invalid="true"] {
		border: 2px solid #999999 !important;
		outline: none !important;
		box-shadow: none !important;
	}

	/* Suppress container-level styling just in case */
	div[data-baseweb="input"] {
		box-shadow: none !important;
		outline: none !important;
	}
	</style>
""", unsafe_allow_html=True)

st.title("<<domAIn chatbot>>")
st.markdown("Ask the domAIn Chatbot anything about the book")

# Chat input
user_input = st.text_input("You:", placeholder="Ask a question...")

# Send button
if st.button("Send"):
	if not user_input.strip():
		st.warning("Please enter a message.")
	else:
		# Show spinner while waiting for response
		with st.spinner("Thinking..."):
			# Prepare request
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

				# Parse and show chatbot response
				data = response.json()
				message = data["outputs"][0]["outputs"][0]["results"]["message"]["text"]
				st.markdown(f"**Chatbot says:** {message}")

			except Exception as e:
				st.error(f"Error: {e}")

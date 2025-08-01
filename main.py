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

st.title("📘 Domain Chatbot")
st.markdown("Ask me anything about the novel *Domain* by Rohan Gavin!")

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
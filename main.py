import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("LANGFLOW_API_KEY", st.secrets.get("LANGFLOW_API_KEY", ""))

if not api_key:
	st.error("❌ LANGFLOW_API_KEY not found.")
	st.stop()

url = "https://langflow-ai-3zj2x.ondigitalocean.app/api/v1/run/177d208c-0608-4386-bc35-2e79ac3f46c7"

st.set_page_config(page_title="<<domAIn chatbot>>", layout="centered")

# CSS: grey input styling + watermark removal
st.markdown("""
	<style>
	div[data-baseweb="input"] { border: 2px solid #999999 !important; border-radius: 12px !important; padding: 0.5rem !important; background-color: #f9f9f9 !important; }
	div[data-baseweb="input"] > div { background-color: transparent !important; border: none !important; padding: 0 !important; box-shadow: none !important; }
	input { background-color: transparent !important; color: #333 !important; font-size:16px !important; outline: none !important; border: none !important; box-shadow: none !important; }
	div[data-baseweb="input"]:focus-within { border: 2px solid #666 !important; }
	#MainMenu, footer, header {visibility:hidden;}
	</style>
""", unsafe_allow_html=True)

st.title("<<domAIn chatbot>>")
st.markdown("Ask the domAIn Chatbot anything about the book")

if "messages" not in st.session_state:
	st.session_state.messages = []

# Display chat history using Streamlit's chat components
for msg in st.session_state.messages:
	with st.chat_message(msg["role"]):
		st.markdown(msg["content"])

# Input widget from Streamlit tutorial
prompt = st.chat_input("Enter your question...")

if prompt:
	st.session_state.messages.append({"role": "user", "content": prompt})
	with st.chat_message("assistant"):
		with st.spinner("Thinking..."):
			try:
				resp = requests.post(url, json={
					"output_type": "chat",
					"input_type": "chat",
					"input_value": prompt
				}, headers={"Content-Type": "application/json","x-api-key": api_key})
				resp.raise_for_status()
				data = resp.json()
				reply = data["outputs"][0]["outputs"][0]["results"]["message"]["text"]
			except Exception as e:
				reply = f"Error: {e}"
			st.markdown(reply)
	st.session_state.messages.append({"role": "assistant", "content": reply})

# Optional clear button
if st.button("Clear chat"):
	st.session_state.messages = []

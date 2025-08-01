import requests
import os
from dotenv import load_dotenv

os.system('clear')
load_dotenv()

# Load API key
try:
	api_key = os.environ["LANGFLOW_API_KEY"]
except KeyError:
	raise ValueError("LANGFLOW_API_KEY environment variable not found. Please set your API key in the environment variables.")

# Langflow endpoint
url = "https://langflow-ai-3zj2x.ondigitalocean.app/api/v1/run/177d208c-0608-4386-bc35-2e79ac3f46c7"

# Headers
headers = {
	"Content-Type": "application/json",
	"x-api-key": api_key
}

print("<< Welcome to the domAIn chatbot >>")

while True:
	user_input = input("You: ")
	if user_input.lower() in ["exit", "quit"]:
		print("Goodbye!")
		break

	payload = {
		"output_type": "chat",
		"input_type": "chat",
		"input_value": user_input
	}

	try:
		response = requests.post(url, json=payload, headers=headers)
		response.raise_for_status()
		data = response.json()
		message = data["outputs"][0]["outputs"][0]["results"]["message"]["text"]
		print("domAIn says:", message)
	except Exception as e:
		print("Oops! Something went wrong:", e)
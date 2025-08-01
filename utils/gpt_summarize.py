from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()  # Load environment varipables from .env file

print("Attempting to initialize OpenAI client...")

# 2. Initialize the client
# The client will automatically look for the OPENAI_API_KEY in your environment.
try:
    client = OpenAI()
    print("Client initialized successfully.")
except Exception as e:
    print(f"Error: Failed to initialize the OpenAI client.")
    print(f"Please check if your OPENAI_API_KEY is set correctly in your .env file.")
    print(f"Details: {e}")
    exit() # Stop the script if the client can't be created


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



def summarize_text(text):
    response = client.chat.completions.create(model="gpt-4o",
    messages=[
        {"role": "system", "content": "Summarize this lecture in student-friendly notes."},
        {"role": "user", "content": text}
    ])
    return response.choices[0].message.content.strip()

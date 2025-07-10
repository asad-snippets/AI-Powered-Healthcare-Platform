import requests
import os
from dotenv import load_dotenv

# Specify the path to your .env file
dotenv_path = 'E:/FYP/Django/Health-Care-Project/.env'
load_dotenv(dotenv_path)

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')  # Make sure your .env file has GEMINI_API_KEY=your_key

def call_gemini_api(messages):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    
    payload = {
        "contents": messages,
        "generationConfig": {
            "maxOutputTokens": 100
        }
    }

    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'}, json=payload)
        response.raise_for_status()
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

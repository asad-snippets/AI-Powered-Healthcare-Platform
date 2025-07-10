import requests

GEMINI_API_KEY = "AIzaSyC8f6Jt9S_u5ijM7uLj4CY8AdssALAJH4w"  # Replace with your real API key

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

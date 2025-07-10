from itertools import zip_longest
import streamlit as st
from streamlit_chat import message
import requests
import json

# === Configuration ===
st.set_page_config(page_title="Health Care Assistant", page_icon="💊", layout="wide")
st.title("Health Care Assistant Bot")

GEMINI_API_KEY = "AIzaSyC8f6Jt9S_u5ijM7uLj4CY8AdssALAJH4w"  # Replace with your actual API key

# === Initialize session state ===
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'entered_prompt' not in st.session_state:
    st.session_state['entered_prompt'] = ""


# === Gemini API Call Function ===
def call_gemini_api(messages):
    if not GEMINI_API_KEY:
        return "❌ API Key is missing."

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


# === Build Gemini Message List ===
def build_gemini_messages():
    system_instruction = (
        "Your name is Health Care Assistant. You assist users with health, symptoms, and disease-related queries." \
        "If user ask you question other topics question then reply him politey that i am a Health care Assistant built to assist you health related quries." \
        "Dont use harsh words, be polite easy and simple."
        "Keep replies under 100 words, stay polite, and stay on topic."
    )

    messages = []

    if not st.session_state['past'] and st.session_state['entered_prompt']:
        first_message = system_instruction + "\n\n" + st.session_state['entered_prompt']
        messages.append({"role": "user", "parts": [{"text": first_message}]})
    else:
        messages.append({"role": "user", "parts": [{"text": system_instruction}]})
        messages.append({"role": "model", "parts": [{"text": "Sure! How can I help you with your health today?"}]})

        for user, bot in zip_longest(st.session_state['past'], st.session_state['generated']):
            if user:
                messages.append({"role": "user", "parts": [{"text": user}]})
            if bot:
                messages.append({"role": "model", "parts": [{"text": bot}]})

    return messages


# === Generate Bot Response ===
def generate_response():
    messages = build_gemini_messages()
    return call_gemini_api(messages)


# === Submit User Query ===
def submit():
    st.session_state.entered_prompt = st.session_state.prompt_input
    st.session_state.prompt_input = ""


# === User Input Box ===
st.text_input("👤 You:", key="prompt_input", on_change=submit)
st.button("📤 Submit")

# === Handle Prompt Submission ===
if st.session_state.entered_prompt != "":
    user_input = st.session_state.entered_prompt
    st.session_state.past.append(user_input)

    bot_reply = generate_response()
    st.session_state.generated.append(bot_reply)

# === Chat Display ===
if st.session_state['generated']:
    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        message(st.session_state['generated'][i], key=f"bot_{i}")
        message(st.session_state['past'][i], is_user=True, key=f"user_{i}")

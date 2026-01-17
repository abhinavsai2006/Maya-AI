import os
import sys
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def ask_ai(prompt):
    """Try multiple AI providers in order and return first valid answer."""
    # GROQ
    if GROQ_API_KEY:
        try:
            r = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": "You are Maya, a helpful Indian AI assistant. Give short, clear answers in 1-2 sentences."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 150
                },
                timeout=5
            )
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"].strip()
        except Exception:
            pass

    # OpenRouter
    if OPENROUTER_API_KEY:
        try:
            r = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"},
                json={
                    "model": "meta-llama/llama-3.1-8b-instruct:free",
                    "messages": [
                        {"role": "system", "content": "You are Maya, a helpful Indian AI assistant. Give short, clear answers in 1-2 sentences."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 150
                },
                timeout=6
            )
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"].strip()
        except Exception:
            pass

    # Gemini (Google)
    if GEMINI_API_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
            r = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [{"parts": [{"text": f"You are Maya, a helpful Indian AI assistant. Give short, clear answers in 1-2 sentences.\n\nUser: {prompt}"}]}],
                    "generationConfig": {"temperature": 0.7, "maxOutputTokens": 150}
                },
                timeout=15
            )
            if r.status_code == 200:
                j = r.json()
                if "candidates" in j and j["candidates"]:
                    return j["candidates"][0]["content"]["parts"][0]["text"].strip()
                if "output" in j and "candidates" in j["output"]:
                    return j["output"]["candidates"][0]["content"][0]["text"].strip()
                return str(j)
        except Exception:
            pass

    return "Sorry, I am unable to think right now. Please check my API keys."

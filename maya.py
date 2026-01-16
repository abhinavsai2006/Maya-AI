import speech_recognition as sr
import asyncio
import edge_tts
import pygame
import os
import requests

# -------------------------------------------------------
# AI INTELLIGENCE – Multi-Provider LLM Integration
# -------------------------------------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def ask_ai(prompt):
    """
    Try multiple AI providers in order (fastest first).
    Returns the first successful response.
    """
    
    # ---- 1️⃣ GROQ (FASTEST - Llama 3) ----
    if GROQ_API_KEY:
        try:
            r = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
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
        except Exception as e:
            print(f"[Groq Error] {e}")
    
    # ---- 2️⃣ OPENROUTER (FALLBACK) ----
    if OPENROUTER_API_KEY:
        try:
            r = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                },
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
        except Exception as e:
            print(f"[OpenRouter Error] {e}")
    
    # ---- 3️⃣ GEMINI (GOOGLE) ----
    if GEMINI_API_KEY:
        try:
            r = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}",
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [{
                        "parts": [{"text": f"You are Maya, a helpful Indian AI assistant. Give short, clear answers in 1-2 sentences.\n\nUser: {prompt}"}]
                    }],
                    "generationConfig": {
                        "temperature": 0.7,
                        "maxOutputTokens": 150
                    }
                },
                timeout=6
            )
            if r.status_code == 200:
                return r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        except Exception as e:
            print(f"[Gemini Error] {e}")
    
    return "Sorry, I am unable to think right now. Please check my API keys."

# -------------------------------------------------------
# EDGE TTS – Indian Female Neural Voice (Neerja)
# -------------------------------------------------------
VOICE = "en-IN-NeerjaNeural"
AUDIO_FILE = "maya_voice.mp3"

pygame.mixer.init()

async def speak_async(text):
    """Convert text to speech using Microsoft Edge TTS."""
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(AUDIO_FILE)

def speak(text):
    """Speak text using Indian female neural voice."""
    print(f"MAYA: {text}")
    asyncio.run(speak_async(text))
    
    # Play audio
    pygame.mixer.music.load(AUDIO_FILE)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.delay(100)
    
    pygame.mixer.music.unload()
    
    # Clean up
    try:
        os.remove(AUDIO_FILE)
    except:
        pass

# -------------------------------------------------------
# SPEECH RECOGNITION
# -------------------------------------------------------
recognizer = sr.Recognizer()
recognizer.pause_threshold = 0.8
recognizer.energy_threshold = 200
microphone = sr.Microphone()

# Calibrate once at startup
print("Calibrating microphone...")
with microphone as source:
    recognizer.adjust_for_ambient_noise(source, duration=1)
print("Ready!\n")

def listen():
    """Listen to user and return text."""
    try:
        with microphone as source:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        
        text = recognizer.recognize_google(audio, language="en-IN")
        return text.lower()
    except sr.UnknownValueError:
        return None
    except sr.WaitTimeoutError:
        return None
    except:
        return None

# -------------------------------------------------------
# MAIN LOOP
# -------------------------------------------------------
speak("Hello, I am Maya. I am listening.")

while True:
    print("Listening...")
    user_input = listen()
    
    if not user_input:
        continue
    
    print(f"YOU: {user_input}")
    
    # Exit commands
    if "bye" in user_input or "exit" in user_input or "quit" in user_input:
        speak("Goodbye. Talk to you later.")
        break
    
    # Get AI response
    print("[AI] Thinking...")
    response = ask_ai(user_input)
    speak(response)

import os
import speech_recognition as sr

recognizer = sr.Recognizer()
recognizer.pause_threshold = 0.8
recognizer.energy_threshold = 200

def init_microphone():
    force_text = os.getenv("FORCE_TEXT_INPUT", "0").strip() == "1"
    if force_text:
        return None, True
    try:
        microphone = sr.Microphone()
        return microphone, False
    except Exception:
        return None, True

def calibrate(microphone):
    if microphone is None:
        return
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

def listen(microphone, use_text_input: bool):
    if use_text_input:
        try:
            return input().strip().lower()
        except Exception:
            return None
    try:
        with microphone as source:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        text = recognizer.recognize_google(audio, language="en-IN")
        return text.lower()
    except Exception:
        return None

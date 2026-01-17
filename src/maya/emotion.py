"""
Emotion and personality module for Maya AI.
Adds time-based greetings, emotion detection, and personality traits.
"""

import datetime
import random
from typing import Dict, List


# Personality traits
PERSONALITY_TRAITS = {
    "friendly": True,
    "helpful": True,
    "curious": True,
    "enthusiastic": True,
    "patient": True,
    "humorous": True,
}


def get_time_based_greeting() -> str:
    """Get greeting based on time of day."""
    hour = datetime.datetime.now().hour
    
    if 5 <= hour < 12:
        greetings = [
            "Good morning!",
            "Rise and shine!",
            "Hello! Hope you had a great sleep!",
            "Good morning! Ready to start the day?",
        ]
    elif 12 <= hour < 17:
        greetings = [
            "Good afternoon!",
            "Hello there!",
            "Hey! How's your day going?",
            "Good afternoon! Hope you're having a productive day!",
        ]
    elif 17 <= hour < 21:
        greetings = [
            "Good evening!",
            "Hello! How was your day?",
            "Evening! Time to relax?",
            "Good evening! Hope you had a great day!",
        ]
    else:
        greetings = [
            "Good night!",
            "Hello! Still awake?",
            "Hey night owl!",
            "Evening! Working late?",
        ]
    
    return random.choice(greetings)


def detect_emotion(text: str) -> str:
    """
    Detect user's emotion from text.
    Returns: happy, sad, angry, frustrated, excited, neutral, confused, grateful
    """
    text_lower = text.lower()
    
    # Positive emotions
    if any(word in text_lower for word in ["thanks", "thank you", "grateful", "appreciate", "awesome", "great", "excellent", "love", "wonderful"]):
        return "grateful"
    
    if any(word in text_lower for word in ["yay", "woohoo", "amazing", "fantastic", "excited", "can't wait", "!!!!"]):
        return "excited"
    
    if any(word in text_lower for word in ["happy", "glad", "joy", "pleased", "😊", "😄", ":)"]):
        return "happy"
    
    # Negative emotions
    if any(word in text_lower for word in ["sad", "unhappy", "depressed", "down", "😢", "😞", ":("]):
        return "sad"
    
    if any(word in text_lower for word in ["angry", "mad", "furious", "pissed", "hate", "annoying"]):
        return "angry"
    
    if any(word in text_lower for word in ["frustrated", "annoyed", "irritated", "stuck", "problem", "issue", "not working", "doesn't work"]):
        return "frustrated"
    
    # Confusion
    if any(word in text_lower for word in ["confused", "don't understand", "what does", "how do", "help", "?"]):
        return "confused"
    
    return "neutral"


def get_empathetic_response(emotion: str) -> str:
    """Get an empathetic response based on detected emotion."""
    responses = {
        "grateful": [
            "You're very welcome!",
            "Happy to help!",
            "Anytime! That's what I'm here for!",
            "My pleasure!",
        ],
        "excited": [
            "That's fantastic!",
            "Love your enthusiasm!",
            "That's amazing!",
            "I'm excited too!",
        ],
        "happy": [
            "That's wonderful!",
            "I'm glad to hear that!",
            "Great to see you happy!",
            "That's awesome!",
        ],
        "sad": [
            "I'm sorry to hear that.",
            "That sounds tough. I'm here if you need help.",
            "Is there anything I can do to help?",
            "Hope things get better soon.",
        ],
        "angry": [
            "I understand you're upset.",
            "Let me try to help you with that.",
            "I'm sorry for the frustration.",
            "Let's see what we can do about this.",
        ],
        "frustrated": [
            "I understand that can be frustrating.",
            "Let me help you solve this problem.",
            "Don't worry, we'll figure this out together.",
            "I'm here to help make this easier.",
        ],
        "confused": [
            "Let me explain that better.",
            "No worries, I'm here to help you understand.",
            "Let me break that down for you.",
            "I'll try to make this clearer.",
        ],
        "neutral": [
            "",  # No special response needed
        ],
    }
    
    emotion_responses = responses.get(emotion, responses["neutral"])
    if emotion_responses and emotion_responses[0]:
        return random.choice(emotion_responses)
    return ""


def add_personality_to_response(response: str, emotion: str = "neutral") -> str:
    """Add personality traits to AI response."""
    if not PERSONALITY_TRAITS["friendly"]:
        return response
    
    # Add enthusiasm for certain topics
    if PERSONALITY_TRAITS["enthusiastic"]:
        if any(word in response.lower() for word in ["great", "awesome", "excellent", "perfect"]):
            response = response + " 😊"
    
    # Add humor occasionally
    if PERSONALITY_TRAITS["humorous"] and random.random() < 0.1:
        humor_additions = [
            " (Just kidding!)",
            " Hope that helps!",
            " Cool, right?",
        ]
        if emotion == "happy" or emotion == "excited":
            response = response + random.choice(humor_additions)
    
    return response


def get_casual_acknowledgment() -> str:
    """Get a casual acknowledgment phrase."""
    acknowledgments = [
        "Got it!",
        "Sure thing!",
        "On it!",
        "You got it!",
        "Absolutely!",
        "No problem!",
        "Right away!",
        "Coming right up!",
    ]
    return random.choice(acknowledgments)


def should_ask_follow_up(emotion: str) -> bool:
    """Determine if Maya should ask a follow-up question."""
    if emotion in ["sad", "frustrated", "angry"]:
        return random.random() < 0.3  # 30% chance for negative emotions
    elif emotion in ["excited", "happy"]:
        return random.random() < 0.1  # 10% chance for positive emotions
    return False


def get_follow_up_question(emotion: str) -> str:
    """Get a follow-up question based on emotion."""
    follow_ups = {
        "sad": [
            "Is there anything else I can help with to cheer you up?",
            "Would you like to talk about it?",
        ],
        "frustrated": [
            "Is there anything else causing you trouble?",
            "Would you like me to explain something differently?",
        ],
        "angry": [
            "Is there anything I can do to help resolve this?",
            "Would you like me to try a different approach?",
        ],
        "excited": [
            "What else would you like to do?",
            "Want to try something else fun?",
        ],
        "happy": [
            "What else can I help you with today?",
            "Anything else you'd like to do?",
        ],
    }
    
    questions = follow_ups.get(emotion, [])
    if questions:
        return random.choice(questions)
    return ""


def get_personality_traits() -> Dict[str, bool]:
    """Get current personality traits."""
    return PERSONALITY_TRAITS.copy()


def set_personality_trait(trait: str, value: bool):
    """Set a personality trait."""
    if trait in PERSONALITY_TRAITS:
        PERSONALITY_TRAITS[trait] = value

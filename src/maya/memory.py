"""Memory system for Maya - stores conversation history and user preferences."""
import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

MEMORY_FILE = "maya_memory.json"

class Memory:
    def __init__(self):
        self.short_term = []  # Recent conversation
        self.long_term = {}   # User preferences, name, habits
        self.load()
    
    def load(self):
        """Load memory from file."""
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.short_term = data.get("short_term", [])[-20:]  # Keep last 20
                    self.long_term = data.get("long_term", {})
            except:
                pass
    
    def save(self):
        """Save memory to file."""
        try:
            with open(MEMORY_FILE, "w", encoding="utf-8") as f:
                json.dump({
                    "short_term": self.short_term[-20:],  # Keep last 20
                    "long_term": self.long_term,
                }, f, indent=2, ensure_ascii=False)
        except:
            pass
    
    def add_interaction(self, user_input: str, maya_response: str):
        """Add a conversation turn to short-term memory."""
        self.short_term.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "maya": maya_response,
        })
        if len(self.short_term) > 20:
            self.short_term = self.short_term[-20:]
        self.save()
    
    def set_preference(self, key: str, value: Any):
        """Store a long-term preference or fact about the user."""
        self.long_term[key] = value
        self.save()
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Retrieve a stored preference."""
        return self.long_term.get(key, default)
    
    def get_context(self) -> str:
        """Get conversation context for AI."""
        context = []
        
        # Add user info if available
        if "name" in self.long_term:
            context.append(f"User's name: {self.long_term['name']}")
        if "preferences" in self.long_term:
            prefs = self.long_term["preferences"]
            if prefs:
                context.append(f"Preferences: {', '.join(f'{k}: {v}' for k, v in prefs.items())}")
        
        # Add recent conversation
        if self.short_term:
            recent = self.short_term[-3:]  # Last 3 exchanges
            context.append("Recent conversation:")
            for turn in recent:
                context.append(f"User: {turn['user']}")
                context.append(f"Maya: {turn['maya']}")
        
        return "\n".join(context) if context else ""

# Global memory instance
_memory = Memory()

def get_memory() -> Memory:
    """Get the global memory instance."""
    return _memory

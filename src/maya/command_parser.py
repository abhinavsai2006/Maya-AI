"""Intelligent command parser using AI to understand user intent."""
import os
import json
from typing import Optional, Dict, Any
from . import ai

def parse_command(user_input: str) -> Optional[Dict[str, Any]]:
    """
    Use AI to parse natural language commands into structured actions.
    Returns: {"action": "open_app", "target": "word"} or None if conversational.
    """
    prompt = f"""You are Maya's command parser. Analyze this user input and determine if it's a system action command or a conversation.

User input: "{user_input}"

If it's a system action, respond with ONLY a JSON object in this format:
{{"action": "ACTION_TYPE", "target": "TARGET", "params": {{}}}}"

ACTION_TYPES:
- open_app: open an application (target: app name like "word", "excel", "whatsapp", "chrome")
- open_url: open a website (target: full URL or domain)
- open_settings: open system settings
- lock_screen: lock the computer
- shutdown: shutdown computer
- restart: restart computer
- set_volume: set volume (params: {{"level": 0-100}})
- run_command: run shell command (target: command string)
- search_web: search on web (target: search query)
- send_whatsapp: send WhatsApp message (target: contact, params: {{"message": "text"}})
- read_whatsapp: read WhatsApp messages (target: contact)
- check_whatsapp: check unread WhatsApp messages
- take_screenshot: take a screenshot
- analyze_screen: analyze what's on screen using OCR
- extract_text: extract text from screen using OCR
- copy_text: copy text to clipboard (target: text)
- paste_text: get text from clipboard
- copy_file: copy file/folder (target: source, params: {{"destination": "path"}})
- move_file: move file/folder (target: source, params: {{"destination": "path"}})
- delete_file: delete file/folder (target: path)
- create_folder: create new folder (target: path)
- list_processes: list running processes
- kill_process: kill a process (target: process name or ID)
- get_system_info: get system information
- empty_recycle_bin: empty recycle bin
- conversation: just talking/asking questions (no system action needed)

Examples:
"open microsoft word" -> {{"action": "open_app", "target": "word"}}
"launch chrome browser" -> {{"action": "open_app", "target": "chrome"}}
"go to youtube.com" -> {{"action": "open_url", "target": "https://youtube.com"}}
"lock my computer" -> {{"action": "lock_screen"}}
"set volume to 50" -> {{"action": "set_volume", "params": {{"level": 50}}}}
"what is the weather" -> {{"action": "conversation"}}
"tell me a joke" -> {{"action": "conversation"}}

Respond with ONLY the JSON object, no explanation."""

    try:
        response = ai.ask_ai(prompt).strip()
        # Try to extract JSON from response
        if response.startswith("{") and response.endswith("}"):
            parsed = json.loads(response)
            if parsed.get("action") == "conversation":
                return None
            return parsed
        # Try to find JSON in response
        start = response.find("{")
        end = response.rfind("}") + 1
        if start >= 0 and end > start:
            json_str = response[start:end]
            parsed = json.loads(json_str)
            if parsed.get("action") == "conversation":
                return None
            return parsed
    except Exception as e:
        print(f"[Command Parser] Failed to parse: {e}")
    
    return None

import os
import sys
from . import ai, tts, speech, system_control, command_parser, app_discovery, memory, advanced_control, emotion
try:
    from . import whatsapp, vision, offline_ai, platform_support
    EXTRA_MODULES = True
except ImportError:
    EXTRA_MODULES = False
from typing import Optional

def _check_api_key():
    """Check if Gemini API key is set. Exit if not found."""
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        print("\n" + "="*60)
        print("⚠️  ERROR: GEMINI_API_KEY is required!")
        print("="*60)
        print("\nMaya requires a Google Gemini API key to function.")
        print("\nSteps to fix:")
        print("  1. Get a free API key from: https://makersuite.google.com/app/apikey")
        print("  2. Set the environment variable:")
        print("\n     Windows PowerShell:")
        print("       $env:GEMINI_API_KEY=\"your_api_key_here\"")
        print("\n     Windows CMD:")
        print("       set GEMINI_API_KEY=your_api_key_here")
        print("\n  3. Run Maya again: .\\start_maya.bat")
        print("\n" + "="*60)
        sys.exit(1)
    return api_key

def _handle_system_commands(text: str) -> Optional[str]:
    """Use AI to parse commands intelligently."""
    cmd = command_parser.parse_command(text)
    if cmd is None:
        return None  # It's conversational, let AI handle it
    
    action = cmd.get("action")
    target = cmd.get("target", "")
    params = cmd.get("params", {})
    
    try:
        if action == "open_app":
            # Use app discovery to find the app
            app_path = app_discovery.find_app(target)
            return system_control.open_app(app_path)
        
        elif action == "open_url":
            if not target.startswith("http"):
                target = f"https://{target}"
            return system_control.open_url(target)
        
        elif action == "open_settings":
            return system_control.open_settings()
        
        elif action == "lock_screen":
            return system_control.lock_screen()
        
        elif action == "shutdown":
            return system_control.shutdown(restart=False)
        
        elif action == "restart":
            return system_control.shutdown(restart=True)
        
        elif action == "set_volume":
            level = params.get("level", 50)
            return system_control.set_volume(level)
        
        elif action == "run_command":
            return system_control.run_command(target)
        
        elif action == "search_web":
            url = f"https://www.google.com/search?q={target.replace(' ', '+')}"
            return system_control.open_url(url)
        
        # Advanced control operations
        elif action == "take_screenshot":
            return advanced_control.take_screenshot()
        
        elif action == "copy_text":
            return advanced_control.copy_to_clipboard(target)
        
        elif action == "paste_text":
            return advanced_control.paste_from_clipboard()
        
        elif action == "copy_file":
            dest = params.get("destination", "")
            return advanced_control.copy_file(target, dest)
        
        elif action == "move_file":
            dest = params.get("destination", "")
            return advanced_control.move_file(target, dest)
        
        elif action == "delete_file":
            return advanced_control.delete_file(target)
        
        elif action == "create_folder":
            return advanced_control.create_folder(target)
        
        elif action == "list_processes":
            return advanced_control.list_running_processes()
        
        elif action == "kill_process":
            return advanced_control.kill_process(target)
        
        elif action == "get_system_info":
            return advanced_control.get_system_info()
        
        elif action == "empty_recycle_bin":
            return advanced_control.empty_recycle_bin()
        
        # WhatsApp commands (Phase 6)
        elif action == "send_whatsapp":
            if EXTRA_MODULES:
                message = params.get("message", "")
                return whatsapp.send_whatsapp_message(target, message)
            return "WhatsApp module not installed. Run: pip install selenium"
        
        elif action == "read_whatsapp":
            if EXTRA_MODULES:
                return whatsapp.read_whatsapp_messages(target)
            return "WhatsApp module not installed"
        
        elif action == "check_whatsapp":
            if EXTRA_MODULES:
                return whatsapp.check_unread_whatsapp()
            return "WhatsApp module not installed"
        
        # Vision commands (Phase 7)
        elif action == "analyze_screen":
            if EXTRA_MODULES:
                return vision.analyze_screen_content(ai)
            return "Vision module not installed. Run: pip install pytesseract"
        
        elif action == "extract_text":
            if EXTRA_MODULES:
                text = vision.extract_text_from_screen()
                return text if text else "Could not extract text from screen"
            return "Vision module not installed"
        
        else:
            return None
    except Exception as e:
        return f"Error executing command: {e}"


def run():
    # Check API key before starting
    _check_api_key()
    
    mem = memory.get_memory()
    microphone, use_text_input = speech.init_microphone()

    if not use_text_input and microphone is not None:
        print("Calibrating microphone...")
        speech.calibrate(microphone)
        print("Ready!\n")
    else:
        print("Microphone unavailable. Switching to text input mode.\n")

    # Personalized greeting with time and emotion
    user_name = mem.get_preference("name")
    time_greeting = emotion.get_time_based_greeting()
    if user_name:
        greeting = f"{time_greeting} {user_name}, I am Maya. How can I help you today?"
    else:
        greeting = f"{time_greeting} I am Maya. How can I help you today?"
    tts.speak(greeting)
    
    # Discover apps on first run
    print("[Initializing] Discovering installed applications...")
    app_discovery.discover_apps()
    print("[Ready] Type your commands naturally - I'll understand!")

    while True:
        print("Listening...")
        user_input = speech.listen(microphone, use_text_input)
        if not user_input:
            continue
        print(f"YOU: {user_input}")

        # Exit commands
        if any(x in user_input.lower() for x in ("bye", "exit", "quit", "goodbye")):
            tts.speak("Goodbye. Talk to you later.")
            break

        # Try system commands first
        sys_result = _handle_system_commands(user_input)
        if sys_result is not None:
            # Add empathy for the action
            user_emotion = emotion.detect_emotion(user_input)
            empathy = emotion.get_empathetic_response(user_emotion)
            
            if empathy:
                final_response = f"{empathy} {sys_result}"
            else:
                final_response = sys_result
            
            tts.speak(final_response)
            mem.add_interaction(user_input, final_response)
            continue

        # Detect emotion for better AI response
        user_emotion = emotion.detect_emotion(user_input)
        empathy = emotion.get_empathetic_response(user_emotion)
        
        # Otherwise ask AI with memory context
        print("[AI] Thinking...")
        context = mem.get_context()
        if context:
            prompt = f"{context}\n\nUser: {user_input}"
        else:
            prompt = user_input
        
        response = ai.ask_ai(prompt)
        
        # Add personality and empathy
        if empathy:
            response = f"{empathy} {response}"
        response = emotion.add_personality_to_response(response, user_emotion)
        
        tts.speak(response)
        mem.add_interaction(user_input, response)
        
        # Learn user's name if mentioned
        if "my name is" in user_input.lower():
            parts = user_input.lower().split("my name is")
            if len(parts) > 1:
                name = parts[1].strip().split()[0].capitalize()
                mem.set_preference("name", name)
                print(f"[Memory] Learned user's name: {name}")
        
        # Occasionally ask follow-up questions
        if emotion.should_ask_follow_up(user_emotion):
            follow_up = emotion.get_follow_up_question(user_emotion)
            if follow_up:
                print(f"MAYA: {follow_up}")
                tts.speak(follow_up)

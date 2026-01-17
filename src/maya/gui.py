"""
GUI application for Maya AI.
System tray application with hotkey support.
"""

import os
import sys
import threading
from typing import Optional

try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext, messagebox
    import pystray
    from pystray import MenuItem as item
    from PIL import Image, ImageDraw
    import keyboard
    TKINTER_AVAILABLE = True
    PYSTRAY_AVAILABLE = True
    KEYBOARD_AVAILABLE = True
except ImportError as e:
    print(f"[GUI] Missing dependencies: {e}")
    TKINTER_AVAILABLE = False
    PYSTRAY_AVAILABLE = False
    KEYBOARD_AVAILABLE = False


class MayaGUI:
    """Maya AI GUI application."""
    
    def __init__(self):
        self.window = None
        self.text_input = None
        self.output_text = None
        self.icon = None
        self.is_running = False
        self.hotkey_registered = False
        
        # Import Maya modules
        try:
            from . import ai, speech, tts, system_control, command_parser, app_discovery, memory, emotion
            self.ai = ai
            self.speech = speech
            self.tts = tts
            self.system_control = system_control
            self.command_parser = command_parser
            self.app_discovery = app_discovery
            self.memory = memory
            self.emotion = emotion
        except ImportError:
            print("[GUI] Failed to import Maya modules")
            sys.exit(1)
    
    def create_window(self):
        """Create main window."""
        if not TKINTER_AVAILABLE:
            print("[GUI] Tkinter not available")
            return
        
        self.window = tk.Tk()
        self.window.title("Maya AI Assistant")
        self.window.geometry("600x500")
        self.window.configure(bg="#1e1e1e")
        
        # Header
        header = tk.Label(
            self.window,
            text="🤖 Maya AI",
            font=("Segoe UI", 20, "bold"),
            bg="#1e1e1e",
            fg="#ffffff"
        )
        header.pack(pady=10)
        
        # Output area
        output_frame = tk.Frame(self.window, bg="#1e1e1e")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        tk.Label(
            output_frame,
            text="Conversation:",
            font=("Segoe UI", 10),
            bg="#1e1e1e",
            fg="#888888"
        ).pack(anchor=tk.W)
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="#2d2d2d",
            fg="#ffffff",
            insertbackground="#ffffff",
            state=tk.DISABLED
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Input area
        input_frame = tk.Frame(self.window, bg="#1e1e1e")
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.text_input = tk.Entry(
            input_frame,
            font=("Segoe UI", 11),
            bg="#2d2d2d",
            fg="#ffffff",
            insertbackground="#ffffff",
            relief=tk.FLAT
        )
        self.text_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, ipady=5)
        self.text_input.bind("<Return>", lambda e: self.send_message())
        
        send_button = tk.Button(
            input_frame,
            text="Send",
            font=("Segoe UI", 10, "bold"),
            bg="#0078d4",
            fg="#ffffff",
            relief=tk.FLAT,
            padx=20,
            command=self.send_message
        )
        send_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Status bar
        self.status_label = tk.Label(
            self.window,
            text="Ready | Press Ctrl+Shift+M to show/hide",
            font=("Segoe UI", 9),
            bg="#1e1e1e",
            fg="#888888",
            anchor=tk.W
        )
        self.status_label.pack(fill=tk.X, padx=10, pady=5)
        
        # Window close handler
        self.window.protocol("WM_DELETE_WINDOW", self.hide_window)
        
        # Initial message
        self.add_output("Maya: Hello! I'm Maya, your AI assistant. How can I help you?", "maya")
    
    def add_output(self, text: str, sender: str = "maya"):
        """Add text to output area."""
        if not self.output_text:
            return
        
        self.output_text.configure(state=tk.NORMAL)
        
        # Color coding
        if sender == "user":
            self.output_text.insert(tk.END, f"You: {text}\n\n", "user")
            self.output_text.tag_config("user", foreground="#4ec9b0")
        else:
            self.output_text.insert(tk.END, f"Maya: {text}\n\n", "maya")
            self.output_text.tag_config("maya", foreground="#dcdcaa")
        
        self.output_text.configure(state=tk.DISABLED)
        self.output_text.see(tk.END)
    
    def send_message(self):
        """Handle sending user message."""
        user_input = self.text_input.get().strip()
        if not user_input:
            return
        
        # Clear input
        self.text_input.delete(0, tk.END)
        
        # Add to output
        self.add_output(user_input, "user")
        
        # Update status
        self.status_label.config(text="Thinking...")
        
        # Process in thread to avoid blocking
        thread = threading.Thread(target=self.process_message, args=(user_input,))
        thread.daemon = True
        thread.start()
    
    def process_message(self, user_input: str):
        """Process user message and get response."""
        try:
            # Check for exit
            if any(x in user_input.lower() for x in ("bye", "exit", "quit", "goodbye")):
                self.add_output("Goodbye! Minimizing to system tray. Press Ctrl+Shift+M to show again.", "maya")
                self.window.after(2000, self.hide_window)
                return
            
            # Try system commands first
            cmd = self.command_parser.parse_command(user_input)
            if cmd:
                # Execute system command
                response = self.execute_command(cmd)
                self.add_output(response, "maya")
            else:
                # Ask AI
                mem = self.memory.get_memory()
                context = mem.get_context()
                if context:
                    prompt = f"{context}\n\nUser: {user_input}"
                else:
                    prompt = user_input
                
                response = self.ai.ask_ai(prompt)
                
                # Add emotion
                user_emotion = self.emotion.detect_emotion(user_input)
                empathy = self.emotion.get_empathetic_response(user_emotion)
                if empathy:
                    response = f"{empathy} {response}"
                
                self.add_output(response, "maya")
                
                # Save to memory
                mem.add_interaction(user_input, response)
            
        except Exception as e:
            self.add_output(f"Error: {e}", "maya")
        finally:
            self.status_label.config(text="Ready | Press Ctrl+Shift+M to show/hide")
    
    def execute_command(self, cmd: dict) -> str:
        """Execute system command."""
        action = cmd.get("action")
        target = cmd.get("target", "")
        params = cmd.get("params", {})
        
        try:
            if action == "open_app":
                app_path = self.app_discovery.find_app(target)
                return self.system_control.open_app(app_path)
            elif action == "open_url":
                if not target.startswith("http"):
                    target = f"https://{target}"
                return self.system_control.open_url(target)
            elif action == "lock_screen":
                return self.system_control.lock_screen()
            else:
                return f"Command '{action}' executed"
        except Exception as e:
            return f"Error: {e}"
    
    def create_tray_icon(self):
        """Create system tray icon."""
        if not PYSTRAY_AVAILABLE:
            print("[GUI] pystray not available")
            return
        
        # Create icon image
        width = 64
        height = 64
        color1 = (0, 120, 212)  # Blue
        color2 = (255, 255, 255)  # White
        
        image = Image.new('RGB', (width, height), color1)
        dc = ImageDraw.Draw(image)
        dc.rectangle([width//4, height//4, 3*width//4, 3*height//4], fill=color2)
        
        # Create menu
        menu = (
            item('Show', self.show_window),
            item('Hide', self.hide_window),
            item('Exit', self.quit_app)
        )
        
        # Create icon
        self.icon = pystray.Icon("Maya AI", image, "Maya AI Assistant", menu)
    
    def show_window(self, icon=None, item=None):
        """Show main window."""
        if self.window:
            self.window.deiconify()
            self.window.lift()
            self.window.focus_force()
    
    def hide_window(self):
        """Hide main window to tray."""
        if self.window:
            self.window.withdraw()
    
    def quit_app(self, icon=None, item=None):
        """Quit application."""
        if self.icon:
            self.icon.stop()
        if self.window:
            self.window.quit()
        sys.exit(0)
    
    def register_hotkey(self):
        """Register global hotkey Ctrl+Shift+M."""
        if not KEYBOARD_AVAILABLE:
            print("[GUI] keyboard module not available")
            return
        
        try:
            keyboard.add_hotkey('ctrl+shift+m', self.toggle_window)
            self.hotkey_registered = True
            print("[GUI] Hotkey registered: Ctrl+Shift+M")
        except Exception as e:
            print(f"[GUI] Failed to register hotkey: {e}")
    
    def toggle_window(self):
        """Toggle window visibility."""
        if self.window:
            if self.window.state() == 'withdrawn':
                self.show_window()
            else:
                self.hide_window()
    
    def run(self):
        """Run the GUI application."""
        if not TKINTER_AVAILABLE:
            print("[GUI] Cannot run GUI - tkinter not available")
            return
        
        # Create window
        self.create_window()
        
        # Create tray icon
        if PYSTRAY_AVAILABLE:
            self.create_tray_icon()
            
            # Run tray icon in separate thread
            def run_tray():
                self.icon.run()
            
            tray_thread = threading.Thread(target=run_tray, daemon=True)
            tray_thread.start()
        
        # Register hotkey
        if KEYBOARD_AVAILABLE:
            self.register_hotkey()
        
        # Discover apps
        print("[GUI] Discovering applications...")
        self.app_discovery.discover_apps()
        
        # Run main loop
        self.is_running = True
        self.window.mainloop()


def start_gui():
    """Start Maya GUI application."""
    app = MayaGUI()
    app.run()


if __name__ == "__main__":
    start_gui()

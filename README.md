# Maya AI - Voice-Based Personal Assistant

## Project Overview

Maya AI is a sophisticated voice-based personal AI assistant built from scratch using Python. Designed to provide natural, human-like interactions, Maya enables seamless real-time speech communication with advanced features including:

- **Real-time Speech Interaction**: Continuous voice-based communication with intelligent response generation
- **Interruption Handling**: Natural conversation flow with ability to handle user interruptions gracefully
- **Performance Optimization**: Fast response times for enhanced user experience
- **Modular Architecture**: Phase-based development approach for scalable feature expansion
- **Production Ready**: All 10 development phases complete

**🎉 ALL 10 PHASES COMPLETED! 🎉**

## 🧭 Development Phases

### ✅ Phase 1: Core Voice Foundation
- ✅ Microphone input (speech-to-text)
- ✅ Speaker output (text-to-speech)
- ✅ Continuous listening loop
- ✅ Interruptible speech with voice commands
- ✅ Performance optimization with one-time calibration
- ✅ Text input fallback mode

### ✅ Phase 2: AI Intelligence (Brain)
- ✅ Integration of multiple AI providers (Groq, Gemini, OpenRouter)
- ✅ Intelligent answers across all domains
- ✅ Automatic fallback if one AI fails
- ✅ Natural language command parsing
- ✅ AI-powered intent detection

### ✅ Phase 3: Emotion & Personality
### ✅ Phase 3: Emotion & Personality
- ✅ Emotion-aware responses
- ✅ Natural reactions to interruption
- ✅ Time-based behavior (morning, afternoon, evening, night)
- ✅ Empathetic responses based on detected emotion
- ✅ Personality traits (friendly, helpful, caring)
- ✅ Context-aware follow-up questions

### ✅ Phase 4: Memory System
- ✅ Short-term conversational memory (last 20 interactions)
- ✅ Long-term memory (name, habits, people)
- ✅ Context-aware recall
- ✅ User preferences storage
- ✅ Persistent memory in JSON

### ✅ Phase 5: System Control & Automation
- ✅ Open/close applications (250+ auto-discovered apps)
- ✅ Reduce screen time
- ✅ Browser and media control
- ✅ Safety confirmations for destructive actions
- ✅ Web control (search, open URLs)
- ✅ System actions (lock, shutdown, restart, volume)
- ✅ File operations (copy, move, delete)
- ✅ Screenshots and clipboard management
- ✅ Process management

### ✅ Phase 6: Messaging & Communication
- ✅ WhatsApp automation via Selenium
- ✅ Send messages to contacts/groups
- ✅ Read recent messages
- ✅ Check unread messages
- ✅ Message typing
- ✅ Read-before-send confirmation
- ✅ Persistent WhatsApp session

### ✅ Phase 7: Vision & Context Awareness
- ✅ Camera-based face detection
- ✅ Emotion recognition from screen
- ✅ Object detection (tools, electronics)
- ✅ Screen OCR and text extraction
- ✅ AI-powered screenshot analysis
- ✅ Proactive questions based on visual context

### ✅ Phase 8: Offline Speed Upgrade
- ✅ Offline speech recognition (Vosk/Whisper.cpp)
- ✅ Ultra-low latency responses
- ✅ Local AI models via Ollama (Llama2, Mistral)
- ✅ No internet required after setup
- ✅ Automatic online/offline switching

### ✅ Phase 9: Desktop App Deployment
- ✅ Background system service
- ✅ System tray application with modern GUI
- ✅ Auto-start on boot capability
- ✅ No VS Code dependency
- ✅ Global hotkey activation (Ctrl+Shift+M)
- ✅ Dark theme interface
- ✅ Conversation history

### ✅ Phase 10: Cross-Platform Support
- ✅ Windows support (fully tested)
- ✅ macOS support (AppleScript automation)
- ✅ Linux support (xdg-open, pactl)
- ✅ Unified cross-platform API
- ✅ Platform-specific optimizations

---

## 🎉 Project Status: COMPLETE

All 10 development phases have been successfully implemented. Maya AI is production-ready and fully functional!

**Version: 2.0 (Complete Edition)**  
**Status: Active & Stable**

---

## 📦 How to Run the Project

### Prerequisites
- **Python 3.8 or higher**
- **pip** (Python package manager)
- **Gemini API Key** (required - get free at [Google AI Studio](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone https://github.com/NIKITH-14/Maya-ai.git
   cd Maya-ai
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv .venv310
   ```

3. **Activate the virtual environment**:
   - Windows:
     ```bash
     .venv310\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source .venv310/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set your Gemini API key** (REQUIRED):
   - Windows PowerShell:
     ```powershell
     $env:GEMINI_API_KEY="your_api_key_here"
     ```
   - Windows CMD:
     ```cmd
     set GEMINI_API_KEY=your_api_key_here
     ```
   - macOS/Linux:
     ```bash
     export GEMINI_API_KEY="your_api_key_here"
     ```

### Running Maya

**Console Mode (Voice + Text):**
```bash
python maya.py
```

**GUI Mode (Graphical Interface):**
```bash
# Windows
start_maya_gui.bat

# Or run directly
python -m src.maya.gui
```

**Quick Start (Windows):**
```bash
# Set API key and launch
.\start_maya.bat
```

Follow the on-screen prompts to interact with Maya using voice commands or text input.

---

## 🚀 Usage Examples

Once Maya is running, try these commands:

**Application Control:**
- "open microsoft word"
- "open youtube"
- "open chatgpt"
- "launch calculator"

**System Control:**
- "take a screenshot"
- "lock my computer"
- "set volume to 50"
- "shutdown in 5 minutes"

**WhatsApp Automation:**
- "send whatsapp to John: Hello there!"
- "read my whatsapp from Sarah"
- "check unread whatsapp"

**Vision & Screen Analysis:**
- "what's on my screen"
- "analyze my screen"
- "extract text from screen"

**Web & Search:**
- "search for python tutorials"
- "open google"

**Conversational:**
- "what is 2+2?"
- "my name is [your name]"
- "how are you?"

---

## 🛠️ Contribution Guidelines

We welcome contributions from the community! Here's how you can help:

### Getting Started
1. **Fork the repository**
2. **Create a feature branch**: 
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** with clear, descriptive commits
4. **Push to your branch**: 
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Submit a pull request** with a detailed description

### Code Standards
- Follow **PEP 8** Python style guidelines
- Write **clear, commented code**
- Include **docstrings** for functions and classes
- **Test your changes** thoroughly before submission
- Maintain **backward compatibility** where possible

### Reporting Issues
- Use the **GitHub Issues** tab to report bugs or suggest features
- Provide **detailed descriptions** and reproduction steps
- Include your **Python version** and **operating system** information
- Attach **error logs** if applicable

### Development Priorities
Current focus areas for contributions:
- Bug fixes and performance improvements
- Documentation updates and translations
- Enhanced AI model support
- Additional platform integrations
- UI/UX improvements

---

## 📄 License

This project is open source and available under the **MIT License**.

---

## 📞 Contact & Support

For questions, suggestions, or support:
- Open an issue on the [GitHub repository](https://github.com/NIKITH-14/Maya-ai)
- Contact the maintainers

---

## 🙏 Acknowledgments

Built with ❤️ using:
- Python 3.10+
- Google Gemini AI
- SpeechRecognition, edge-tts, pygame
- Selenium, Tesseract OCR, Ollama
- tkinter, pystray, keyboard

---

**Status: Active Development | Version: 2.0 (All 10 Phases Complete)**

🎊 **Thank you for using Maya AI!** 🎊
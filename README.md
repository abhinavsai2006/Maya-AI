# Maya AI - Voice-Based Personal Assistant

## Project Overview

Maya AI is a sophisticated voice-based personal AI assistant built from scratch using Python. Designed to provide natural, human-like interactions, Maya enables seamless real-time speech communication with advanced features including:

- **Real-time Speech Interaction**: Continuous voice-based communication with intelligent response generation
- **Interruption Handling**: Natural conversation flow with ability to handle user interruptions gracefully
- **Performance Optimization**: Fast response times for enhanced user experience
- **Modular Architecture**: Phase-based development approach for scalable feature expansion

## 🧭 Development Phases

### ✅ Completed

- **Phase 1: Core Voice Foundation**
  - Microphone input (speech-to-text)
  - Speaker output (text-to-speech)
  - Continuous listening loop

- **Phase 1.5: Interruptible Speech**
  - Microphone remains active while Maya is speaking
  - User can interrupt Maya using voice commands like "stop"
  - Immediate speech cancellation (human-like behavior)

- **Phase 1.6: Performance Optimization**
  - One-time microphone calibration
  - Reduced response latency
  - Faster and more natural interaction

---

### 🚧 In Progress / Planned

- **Phase 2: AI Intelligence (Brain)**
  - Integration of multiple AI providers (Groq, Gemini, OpenRouter)
  - Intelligent answers across all domains
  - Automatic fallback if one AI fails

- **Phase 3: Emotion & Personality**
  - Emotion-aware responses
  - Natural reactions to interruption
  - Time-based behavior (tired, caring, annoyed, friendly)

- **Phase 4: Memory System**
  - Short-term conversational memory
  - Long-term memory (name, habits, people)
  - Context-aware recall

- **Phase 5: System Control & Automation**
  - Open/close applications
  - Reduce screen time
  - Browser and media control
  - Safety confirmations

- **Phase 6: Messaging & Communication**
  - WhatsApp and messaging automation
  - Message typing
  - Read-before-send confirmation

- **Phase 7: Vision & Context Awareness**
  - Camera-based face detection
  - Emotion recognition
  - Object detection (e.g., tools, electronics)
  - Proactive questions ("What are you building?")

- **Phase 8: Offline Speed Upgrade**
  - Offline speech recognition (Vosk / Whisper.cpp)
  - Ultra-low latency responses

- **Phase 9: Desktop App Deployment**
  - Background system service
  - System tray application
  - Auto-start on boot
  - No VS Code dependency

## How to Run the Project

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone https://github.com/NIKITH-14/Maya-ai.git
   cd Maya-ai
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running Maya

Execute the main script to start the assistant:
```bash
python maya.py
```

Follow the on-screen prompts to interact with Maya using voice commands.

## Contribution Guidelines

We welcome contributions from the community! Here's how you can help:

### Getting Started
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes with clear, descriptive commits
4. Push to your branch: `git push origin feature/your-feature-name`
5. Submit a pull request with a detailed description

### Code Standards
- Follow PEP 8 Python style guidelines
- Write clear, commented code
- Include docstrings for functions and classes
- Test your changes thoroughly before submission

### Reporting Issues
- Use the GitHub Issues tab to report bugs or suggest features
- Provide detailed descriptions and reproduction steps
- Include your Python version and operating system information

### Development Priorities
Current focus areas for contributions:
- Phase 2: AI Intelligence integration
- Bug fixes and performance improvements
- Documentation updates

## License

This project is open source and available under the MIT License.

## Contact & Support

For questions, suggestions, or support, please open an issue on the GitHub repository or contact the maintainers.

---

**Status**: Active Development | **Version**: 0.3 (Phase 1.6 Complete)
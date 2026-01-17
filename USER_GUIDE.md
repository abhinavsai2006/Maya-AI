# 🎯 Maya AI - Complete User Guide

## What is Maya AI?

Maya is an intelligent personal assistant that understands natural language and controls your Windows PC. Unlike traditional voice assistants with rigid commands, Maya uses AI to understand **any way** you phrase your requests.

---

## ✨ Key Features

### 🧠 **True Natural Language Understanding**
- No memorizing commands - just talk naturally
- "open word" = "launch microsoft word" = "start word app"
- AI figures out what you mean

### 🔍 **Auto-Discovers 250+ Apps**
- Automatically finds all installed applications
- One-time scan on first run
- Works with ANY app on your system

### 💾 **Remembers You**
- Learns your name
- Remembers past conversations
- Context-aware responses

### 🎭 **Has Personality**
- Time-based greetings (morning, evening)
- Detects your mood (happy, frustrated, etc.)
- Responds with empathy

### ⚡ **Complete System Control**
- Launch apps, open websites
- Take screenshots, manage files
- Control processes, system settings
- Lock, shutdown, restart

---

## 📥 Installation (5 Minutes)

### Step 1: Prerequisites
- **Windows 10/11**
- **Python 3.10+** ([Download](https://www.python.org/downloads/))
- **Gemini API Key** ([Get Free Key](https://makersuite.google.com/app/apikey))

### Step 2: Download
```bash
git clone https://github.com/NIKITH-14/Maya-ai.git
cd Maya-ai
```

### Step 3: Setup Environment
```bash
# Create virtual environment
python -m venv .venv310
.venv310\Scripts\activate

# Install dependencies (takes 2-3 minutes)
pip install -r requirements.txt
```

### Step 4: Configure API
```bash
# Set your Gemini API key
set GEMINI_API_KEY=your_key_here

# Optional: Disable TTS for faster testing
set DISABLE_EDGE_TTS=1
set FORCE_TEXT_INPUT=1
```

### Step 5: Launch Maya
```bash
python maya.py
```

**First run**: Maya will scan your system for installed apps (takes 10-20 seconds).

---

## 🎮 Usage Guide

### Starting Maya

**With Microphone** (Voice Mode):
```bash
python maya.py
```

**Text-Only Mode** (Recommended for Testing):
```bash
set FORCE_TEXT_INPUT=1
set DISABLE_EDGE_TTS=1
python maya.py
```

### Talking to Maya

Just type naturally! Maya understands context and intent.

#### 📱 **Opening Apps**
```
✅ "open microsoft word"
✅ "launch chrome browser"
✅ "start spotify"
✅ "open notepad"
✅ "open file explorer"
```

#### 🌐 **Web Control**
```
✅ "go to youtube.com"
✅ "open github"
✅ "search for python tutorials"
✅ "open google"
```

#### 💻 **System Actions**
```
✅ "lock my computer"
✅ "set volume to 50"
✅ "shutdown computer" (asks confirmation)
✅ "restart pc"
✅ "open wifi settings"
```

#### 📸 **Screenshots & Files**
```
✅ "take a screenshot"
✅ "create a folder called Projects"
✅ "copy this text: hello world"
✅ "paste from clipboard"
```

#### ⚙️ **Process Management**
```
✅ "list running processes"
✅ "kill process chrome"
✅ "show system info"
✅ "empty recycle bin"
```

#### 💬 **Conversation**
```
✅ "what's 2+2?"
✅ "tell me a joke"
✅ "how do I learn python?"
✅ "what's the weather today?"
```

#### 🧠 **Memory**
```
✅ "my name is John"
   → Next time: "Hello John!"
✅ Maya remembers your last 20 conversations
```

---

## 🎯 Advanced Features

### Custom App Mappings

If Maya can't find an app, add it manually to `apps.json`:

```json
{
  "whatsapp": "C:\\Users\\YourName\\AppData\\Local\\WhatsApp\\WhatsApp.exe",
  "myapp": "C:\\Path\\To\\Your\\App.exe"
}
```

Then restart Maya.

### Environment Variables

| Variable | Purpose | Values |
|----------|---------|--------|
| `GEMINI_API_KEY` | AI provider (required) | Your API key |
| `FORCE_TEXT_INPUT` | Use text instead of mic | `1` or `0` |
| `DISABLE_EDGE_TTS` | Disable voice output | `1` or `0` |
| `GROQ_API_KEY` | Fallback AI (optional) | Your API key |
| `OPENROUTER_API_KEY` | Fallback AI (optional) | Your API key |

### Personality Customization

Maya's personality can be adjusted in `src/maya/emotion.py`:

```python
PERSONALITY_TRAITS = {
    "friendly": True,
    "helpful": True,
    "curious": True,
    "enthusiastic": True,
    "patient": True,
    "humorous": True,  # Set to False for serious Maya
}
```

---

## 🔧 Troubleshooting

### "Windows cannot find [app]"

**Solution 1**: Run app discovery manually:
```python
from src.maya import app_discovery
app_discovery.discover_apps(force_refresh=True)
```

**Solution 2**: Add to `apps.json`:
```json
{
  "appname": "C:\\Full\\Path\\To\\App.exe"
}
```

### "Sorry, I am unable to think right now"

**Cause**: API key invalid or rate limit hit

**Solution**:
1. Check your API key is correct: `echo %GEMINI_API_KEY%`
2. Get a new key at [Google AI Studio](https://makersuite.google.com/app/apikey)
3. Wait a few minutes if rate limited

### Microphone Not Working

**Solution**: Use text input mode:
```bash
set FORCE_TEXT_INPUT=1
python maya.py
```

### TTS (Voice Output) Issues

**Solution**: Disable TTS (text-only output):
```bash
set DISABLE_EDGE_TTS=1
python maya.py
```

### App Not Found

**Check discovered apps**:
```bash
# View discovered_apps.json
notepad discovered_apps.json
```

**Force re-scan**:
```bash
# Delete cache and restart Maya
del discovered_apps.json
python maya.py
```

---

## 📊 File Structure

```
Maya-AI/
├── maya.py                    # Main entry point - RUN THIS
├── requirements.txt           # Python dependencies
├── apps.json                  # Custom app mappings (create if needed)
├── discovered_apps.json       # Auto-discovered apps (auto-generated)
├── maya_memory.json           # Your conversations (auto-generated)
│
├── src/maya/                  # Core modules
│   ├── app.py                 # Main loop
│   ├── ai.py                  # Multi-AI provider
│   ├── command_parser.py      # Natural language parser
│   ├── app_discovery.py       # App scanner
│   ├── system_control.py      # System operations
│   ├── advanced_control.py    # Files, screenshots, etc.
│   ├── emotion.py             # Personality & emotion
│   ├── memory.py              # Conversation memory
│   ├── speech.py              # Voice input
│   └── tts.py                 # Voice output
│
├── README.md                  # Project documentation
├── DEVELOPMENT_SUMMARY.md     # What's been built
└── USER_GUIDE.md             # This file
```

---

## 🎓 Examples & Tips

### Example Session

```
[Maya starts]
MAYA: Good morning! I am Maya. How can I help you today?

YOU: hi maya
MAYA: Hello! How can I assist you today?

YOU: my name is Sarah
MAYA: Nice to meet you, Sarah!

YOU: open microsoft word
MAYA: Opened C:\Program Files\Microsoft Office\Word.exe

YOU: take a screenshot
MAYA: Screenshot saved to C:\Users\Sarah\Pictures\Maya Screenshots\screenshot_20240115_103045.png

YOU: thanks!
MAYA: You're very welcome! Happy to help! 😊

YOU: bye
MAYA: Goodbye. Talk to you later.
```

### Pro Tips

✅ **Be Natural**: Maya understands context  
✅ **Use Aliases**: "chrome" = "google chrome" = "browser"  
✅ **Ask Questions**: Maya has AI - ask anything!  
✅ **Teach Maya**: Say "my name is [name]" to be remembered  
✅ **Check Logs**: Maya prints what it's doing in console  

---

## 🚀 What's Coming Next

### Phase 6: WhatsApp (In Progress)
- Send messages via WhatsApp Web
- Read messages
- Auto-responses

### Phase 7: Vision
- Screenshot analysis
- OCR text extraction
- Screen understanding

### Phase 8: Offline Mode
- Local AI models (no internet needed)
- Faster responses
- Complete privacy

### Phase 9: Desktop App
- System tray icon
- Hotkey activation (Ctrl+Shift+M)
- No terminal needed

### Phase 10: Cross-Platform
- macOS support
- Linux support

---

## 🤝 Support & Contributing

### Getting Help
- **Issues**: [GitHub Issues](https://github.com/NIKITH-14/Maya-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/NIKITH-14/Maya-ai/discussions)

### Contributing
We welcome contributions! See `README.md` for guidelines.

Focus areas:
- WhatsApp automation
- Vision/OCR features
- GUI development
- Cross-platform support

---

## 📜 License

MIT License - Free to use and modify!

---

## 🎉 Quick Start Recap

1. **Install Python 3.10+**
2. **Clone repo**: `git clone https://github.com/NIKITH-14/Maya-ai.git`
3. **Setup venv**: `python -m venv .venv310 && .venv310\Scripts\activate`
4. **Install deps**: `pip install -r requirements.txt`
5. **Set API key**: `set GEMINI_API_KEY=your_key`
6. **Run Maya**: `python maya.py`
7. **Start talking!** 🎤

---

**Maya AI - Your intelligent personal assistant. Talk naturally, get things done.**

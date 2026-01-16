# Maya AI - Project Structure

## Overview
Maya AI is organized using a modular, scalable architecture designed for easy development, maintenance, and contribution.

## Directory Tree

```
Maya-ai/
│
├── src/                           # Main source code directory
│   ├── maya.py                    # Main entry point (Phase 1–2 logic)
│   │                              # Initialization, voice interaction, core features
│   │
│   ├── voice/                     # Speech processing module
│   │   ├── __init__.py            # Voice module package initialization
│   │   ├── stt.py                 # Speech-to-Text (STT)
│   │   │                          # - Microphone input handling
│   │   │                          # - Audio processing
│   │   │                          # - Speech recognition
│   │   │
│   │   ├── tts.py                 # Text-to-Speech (TTS)
│   │   │                          # - Text-to-audio conversion
│   │   │                          # - Indian female voice output
│   │   │                          # - Audio playback optimization
│   │   │
│   │   └── interrupt.py           # Interrupt / Barge-in Logic
│   │                              # - User interruption handling
│   │                              # - Natural conversation flow
│   │                              # - Graceful interruption management
│   │
│   ├── ai/                        # Artificial Intelligence module
│   │   ├── __init__.py            # AI module package initialization
│   │   └── brain.py               # AI Brain (Intelligence Layer)
│   │                              # - Response generation
│   │                              # - Groq API integration
│   │                              # - Google Gemini integration
│   │                              # - Fallback mechanisms
│   │                              # - Context-aware processing
│   │
│   └── utils/                     # Utilities module
│       ├── __init__.py            # Utils module package initialization
│       └── config.py              # Configuration Management
│                                  # - Environment variables
│                                  # - API keys
│                                  # - Application constants
│
├── docs/                          # Documentation directory
│   ├── roadmap.md                 # Full development roadmap (Phase 1-9)
│   └── setup.md                   # Setup and installation guide
│
├── README.md                       # Project overview and quick start
├── PROJECT_STRUCTURE.md            # This file - project structure documentation
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
├── LICENSE                         # MIT License
└── .git/                          # Git repository (auto-created)
```

## Module Descriptions

### src/maya.py
**Purpose**: Main entry point for the application  
**Responsibilities**:
- Application initialization
- Voice interaction loop
- Phase 1-2 core feature implementation
- Orchestration of voice and AI modules

### src/voice/ (Voice Processing Module)
**Purpose**: Handle all voice input/output and real-time speech interaction

#### stt.py (Speech-to-Text)
- Capture audio from microphone
- Process and convert speech to text
- Handle audio preprocessing
- Manage listening states

#### tts.py (Text-to-Speech)
- Convert text responses to audio
- Support Indian female voice output
- Optimize audio quality and playback
- Handle audio streaming

#### interrupt.py (Interrupt Logic)
- Detect user speech interruptions
- Stop ongoing speech output
- Handle barge-in requests
- Maintain natural conversation flow

### src/ai/ (AI Intelligence Module)
**Purpose**: Provide intelligent response generation and processing

#### brain.py (AI Brain)
- Process user input and generate responses
- Integrate multiple AI APIs:
  - Groq (primary)
  - Google Gemini (secondary)
  - Fallback mechanisms
- Maintain conversation context
- Handle intent recognition and entity extraction

### src/utils/ (Utilities Module)
**Purpose**: Shared utilities and configuration

#### config.py (Configuration)
- Load and manage environment variables
- Store API keys securely
- Define application constants
- Centralize configuration for all modules

## Development Phases

### Completed
- **Phase 1**: Foundation - Core architecture and setup
- **Phase 2**: Speech Recognition - Voice input and basic commands

### In Progress / Planned
- **Phase 3**: Natural Language Processing
- **Phase 4**: Speech Synthesis
- **Phase 5**: Advanced Conversation Features
- **Phase 6**: Smart Features (Calendar, Tasks, etc.)
- **Phase 7**: External Integration (APIs)
- **Phase 8**: Machine Learning Enhancement
- **Phase 9**: Optimization & Deployment

## Key Design Principles

1. **Modularity**: Each component has a single responsibility
2. **Scalability**: Easy to add new features and modules
3. **Maintainability**: Clear separation of concerns
4. **Beginner-Friendly**: Simple structure for new contributors
5. **Extensibility**: Support for future enhancements and integrations

## Getting Started

1. See [README.md](README.md) for quick start
2. See [docs/setup.md](docs/setup.md) for detailed setup instructions
3. See [docs/roadmap.md](docs/roadmap.md) for development roadmap

## Contributing

To contribute:
1. Follow the project structure guidelines
2. Place code in appropriate modules
3. Update documentation as needed
4. See [README.md](README.md) contribution guidelines

---

**Last Updated**: January 16, 2026  
**Current Version**: 0.2 (Phase 2 Complete)

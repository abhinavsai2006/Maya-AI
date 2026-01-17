import os
import asyncio
import pygame

# edge_tts is optional; only used when enabled
try:
    import edge_tts
except Exception:
    edge_tts = None

VOICE = "en-IN-NeerjaNeural"
AUDIO_FILE = "maya_voice.mp3"

# Disable Edge TTS by default; set DISABLE_EDGE_TTS=0 to enable
DISABLE_EDGE_TTS = os.getenv("DISABLE_EDGE_TTS", "1").strip().lower() in ("1", "true", "yes")

tts_available = False
if DISABLE_EDGE_TTS:
    tts_available = False
else:
    try:
        pygame.mixer.init()
        tts_available = True
    except Exception:
        tts_available = False

async def _speak_async(text: str):
    if edge_tts is None:
        raise RuntimeError("edge-tts not installed")
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(AUDIO_FILE)

def speak(text: str):
    """Speak text if TTS enabled; otherwise print only."""
    # Always print full text first
    print(f"MAYA: {text}", flush=True)
    
    if not tts_available:
        return
    
    try:
        asyncio.run(_speak_async(text))
        pygame.mixer.music.load(AUDIO_FILE)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.delay(100)
        pygame.mixer.music.unload()
        try:
            os.remove(AUDIO_FILE)
        except Exception:
            pass
    except Exception as e:
        print(f"[TTS Error] {e} - falling back to text-only output.", flush=True)
        try:
            os.remove(AUDIO_FILE)
        except Exception:
            pass

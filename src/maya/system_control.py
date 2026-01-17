import os
import subprocess
import webbrowser
import ctypes
import json

from typing import Optional

# Confirmation requirement for destructive actions
REQUIRE_CONFIRM = os.getenv("SYSTEM_ACTION_CONFIRM", "1").strip() in ("1", "true", "yes")

# Allow unrestricted commands only when explicitly enabled
ALLOW_UNRESTRICTED = os.getenv("ALLOW_UNRESTRICTED_COMMANDS", "0").strip() in ("1", "true", "yes")

# Optional apps mapping file (JSON) to map friendly names to exact executables/paths
APPS_MAP_FILE = os.path.join(os.getcwd(), "apps.json")
_apps_map = {}
if os.path.exists(APPS_MAP_FILE):
    try:
        with open(APPS_MAP_FILE, "r", encoding="utf-8") as f:
            _apps_map = json.load(f)
    except Exception:
        _apps_map = {}


def _confirm(prompt: str) -> bool:
    if not REQUIRE_CONFIRM:
        return True
    try:
        resp = input(f"{prompt} (yes/no): ").strip().lower()
        return resp in ("y", "yes")
    except Exception:
        return False


def open_settings() -> str:
    """Open Windows Settings."""
    try:
        os.startfile("ms-settings:")
        return "Opened Settings"
    except Exception:
        try:
            subprocess.run('start ms-settings:', shell=True)
            return "Opened Settings"
        except Exception as e:
            return f"Failed to open settings: {e}"


def open_url(url: str) -> str:
    try:
        webbrowser.open(url)
        return f"Opened URL: {url}"
    except Exception as e:
        return f"Failed to open URL: {e}"


def open_app(name_or_path: str) -> str:
    """Open an application by path or friendly name. Use apps.json to map names to paths."""
    try:
        name = name_or_path.strip()
        
        # Check if it's a URL
        if name.startswith("http://") or name.startswith("https://"):
            return open_url(name)
        
        # If exact path exists, open it
        if os.path.exists(name):
            os.startfile(name)
            return f"Opened {name}"

        # Check apps map
        mapped = _apps_map.get(name.lower())
        if mapped:
            if os.path.exists(mapped):
                os.startfile(mapped)
                return f"Opened {name} -> {mapped}"
            else:
                # try start on mapped
                subprocess.run(f'start "" "{mapped}"', shell=True)
                return f"Tried to open mapped {mapped} for {name}"
        # Heuristics / fallbacks
        import shutil, getpass

        # Common aliases
        aliases = {
            "file manager": "explorer",
            "file explorer": "explorer",
            "explorer": "explorer",
            "notebook": "notepad",
            "notepad": "notepad",
            "calculator": "calc",
            "calculator app": "calc",
        }
        lname = name.lower()
        if lname in aliases:
            cmd = aliases[lname]
            try:
                subprocess.run(f'start "" "{cmd}"', shell=True)
                return f"Opened {name} -> {cmd}"
            except Exception:
                pass

        # Check PATH for an executable
        which = shutil.which(name) or shutil.which(name + ".exe")
        if which:
            try:
                os.startfile(which)
                return f"Opened {name} (resolved to {which})"
            except Exception:
                pass

        # Try common WhatsApp install paths under the current user
        user = getpass.getuser()
        whatsapp_candidates = [
            os.path.join(os.path.expanduser(f"~{user}"), "AppData", "Local", "Programs", "WhatsApp", "WhatsApp.exe"),
            os.path.join(os.path.expanduser(f"~{user}"), "AppData", "Local", "WhatsApp", "app-64.0", "WhatsApp.exe"),
            os.path.join(os.path.expanduser(f"~{user}"), "AppData", "Local", "WhatsApp", "WhatsApp.exe"),
        ]
        for cand in whatsapp_candidates:
            if os.path.exists(cand):
                try:
                    os.startfile(cand)
                    return f"Opened {name} -> {cand}"
                except Exception:
                    pass

        # Final fallback: try Windows start with the name (may fail if not registered)
        try:
            cmd = f'start "" "{name}"'
            subprocess.run(cmd, shell=True)
            return f"Tried to open {name} (no mapping found)"
        except Exception as e:
            return f"Failed to open app: {e}"
    except Exception as e:
        return f"Failed to open app: {e}"


def run_command(command: str) -> str:
    """Run an arbitrary shell command. Only allowed without confirmation if ALLOW_UNRESTRICTED=1."""
    cmd = command.strip()
    if not ALLOW_UNRESTRICTED and not _confirm(f"Allow running command: {cmd}?"):
        return "Cancelled"
    try:
        # Run without blocking the assistant; return success message
        subprocess.Popen(cmd, shell=True)
        return f"Executed: {cmd}"
    except Exception as e:
        return f"Failed to execute command: {e}"


def lock_screen() -> str:
    try:
        ctypes.windll.user32.LockWorkStation()
        return "Locked screen"
    except Exception as e:
        return f"Failed to lock screen: {e}"


def shutdown(restart: bool = False) -> str:
    action = "restart" if restart else "shutdown"
    if not _confirm(f"Are you sure you want to {action} the machine?"):
        return "Cancelled"
    try:
        if restart:
            subprocess.run(["shutdown", "/r", "/t", "0"], check=True)
        else:
            subprocess.run(["shutdown", "/s", "/t", "0"], check=True)
        return f"Initiated {action}"
    except Exception as e:
        return f"Failed to {action}: {e}"


def set_volume(level: int) -> str:
    """Set system volume to level 0-100. Best-effort: uses pycaw if available."""
    try:
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        sessions = AudioUtilities.GetSpeakers()
        interface = sessions.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
        # level 0-100 -> scalar 0.0-1.0
        scalar = max(0, min(level, 100)) / 100.0
        volume.SetMasterVolumeLevelScalar(scalar, None)
        return f"Volume set to {level}%"
    except Exception:
        return "Volume control not available (pycaw not installed or unsupported)"

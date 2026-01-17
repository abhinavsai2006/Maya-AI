"""Auto-discover installed applications across Windows systems."""
import os
import winreg
import json
from pathlib import Path
from typing import Dict, List

APPS_CACHE_FILE = "discovered_apps.json"

def _scan_start_menu() -> Dict[str, str]:
    """Scan Windows Start Menu for application shortcuts."""
    apps = {}
    start_menu_paths = [
        os.path.join(os.environ.get("ProgramData", "C:\\ProgramData"), "Microsoft", "Windows", "Start Menu", "Programs"),
        os.path.join(os.environ.get("APPDATA", ""), "Microsoft", "Windows", "Start Menu", "Programs"),
    ]
    
    for base_path in start_menu_paths:
        if not os.path.exists(base_path):
            continue
        try:
            for root, dirs, files in os.walk(base_path):
                for file in files:
                    if file.endswith(".lnk"):
                        app_name = file[:-4].lower()  # Remove .lnk
                        # Simplify name
                        app_name = app_name.replace(" - shortcut", "").strip()
                        full_path = os.path.join(root, file)
                        apps[app_name] = full_path
        except Exception:
            pass
    return apps

def _scan_registry_uninstall() -> Dict[str, str]:
    """Scan Windows registry for installed applications."""
    apps = {}
    reg_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
    ]
    
    for reg_path in reg_paths:
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
            for i in range(winreg.QueryInfoKey(key)[0]):
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    subkey = winreg.OpenKey(key, subkey_name)
                    try:
                        name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                        location = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                        if name and location:
                            apps[name.lower()] = location
                    except:
                        pass
                    winreg.CloseKey(subkey)
                except:
                    pass
            winreg.CloseKey(key)
        except:
            pass
    return apps

def _scan_program_files() -> Dict[str, str]:
    """Scan Program Files directories for executables."""
    apps = {}
    program_paths = [
        os.environ.get("ProgramFiles", "C:\\Program Files"),
        os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"),
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs"),
    ]
    
    for base_path in program_paths:
        if not os.path.exists(base_path):
            continue
        try:
            for item in os.listdir(base_path):
                item_path = os.path.join(base_path, item)
                if os.path.isdir(item_path):
                    # Look for .exe files in this directory
                    try:
                        for file in os.listdir(item_path):
                            if file.endswith(".exe"):
                                app_name = file[:-4].lower()
                                full_path = os.path.join(item_path, file)
                                apps[app_name] = full_path
                                # Also add folder name as alias
                                apps[item.lower()] = full_path
                    except:
                        pass
        except:
            pass
    return apps

def discover_apps(force_refresh: bool = False) -> Dict[str, str]:
    """
    Discover installed applications and cache the results.
    Returns a dictionary mapping app names to their paths/commands.
    """
    if not force_refresh and os.path.exists(APPS_CACHE_FILE):
        try:
            with open(APPS_CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    
    print("[App Discovery] Scanning system for installed applications...")
    apps = {}
    
    # Merge all discovery methods
    apps.update(_scan_start_menu())
    apps.update(_scan_program_files())
    apps.update(_scan_registry_uninstall())
    
    # Add common aliases and web apps
    common_apps = {
        "word": "winword",
        "microsoft word": "winword",
        "excel": "excel",
        "microsoft excel": "excel",
        "powerpoint": "powerpnt",
        "microsoft powerpoint": "powerpnt",
        "notepad": "notepad",
        "calculator": "calc",
        "file explorer": "explorer",
        "explorer": "explorer",
        "cmd": "cmd",
        "command prompt": "cmd",
        "powershell": "powershell",
        "chrome": "chrome",
        "google chrome": "chrome",
        "firefox": "firefox",
        "edge": "msedge",
        "microsoft edge": "msedge",
        # Web apps
        "youtube": "https://www.youtube.com",
        "chatgpt": "https://chat.openai.com",
        "gpt": "https://chat.openai.com",
        "openai": "https://chat.openai.com",
        "gmail": "https://mail.google.com",
        "google": "https://www.google.com",
        "facebook": "https://www.facebook.com",
        "twitter": "https://twitter.com",
        "instagram": "https://www.instagram.com",
        "whatsapp": "https://web.whatsapp.com",
    }
    apps.update(common_apps)
    
    # Cache the results
    try:
        with open(APPS_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(apps, f, indent=2)
        print(f"[App Discovery] Found {len(apps)} applications")
    except:
        pass
    
    return apps

def find_app(app_name: str) -> str:
    """Find the best match for an application name."""
    apps = discover_apps()
    name_lower = app_name.lower().strip()
    
    # Exact match
    if name_lower in apps:
        return apps[name_lower]
    
    # Partial match
    for key, value in apps.items():
        if name_lower in key or key in name_lower:
            return value
    
    # No match - return original name
    return app_name

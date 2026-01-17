"""
Cross-platform support for Maya AI.
Platform detection and OS-specific implementations.
"""

import os
import sys
import platform
import subprocess
from typing import Optional


def get_platform() -> str:
    """
    Get current platform.
    
    Returns:
        'windows', 'macos', or 'linux'
    """
    system = platform.system().lower()
    if system == 'darwin':
        return 'macos'
    return system


def is_windows() -> bool:
    """Check if running on Windows."""
    return get_platform() == 'windows'


def is_macos() -> bool:
    """Check if running on macOS."""
    return get_platform() == 'macos'


def is_linux() -> bool:
    """Check if running on Linux."""
    return get_platform() == 'linux'


def open_app_cross_platform(app_name: str) -> str:
    """
    Open application on any platform.
    
    Args:
        app_name: Name of application
        
    Returns:
        Status message
    """
    try:
        if is_windows():
            # Windows - use start command
            subprocess.Popen(['start', app_name], shell=True)
            return f"Opened {app_name}"
        
        elif is_macos():
            # macOS - use open command
            subprocess.Popen(['open', '-a', app_name])
            return f"Opened {app_name}"
        
        elif is_linux():
            # Linux - try common launchers
            for launcher in ['xdg-open', 'gnome-open', 'kde-open']:
                try:
                    subprocess.Popen([launcher, app_name])
                    return f"Opened {app_name}"
                except FileNotFoundError:
                    continue
            
            # Try direct execution
            subprocess.Popen([app_name])
            return f"Opened {app_name}"
        
        else:
            return f"Unsupported platform: {get_platform()}"
    
    except Exception as e:
        return f"Failed to open {app_name}: {e}"


def open_url_cross_platform(url: str) -> str:
    """
    Open URL in default browser on any platform.
    
    Args:
        url: URL to open
        
    Returns:
        Status message
    """
    import webbrowser
    try:
        webbrowser.open(url)
        return f"Opened {url}"
    except Exception as e:
        return f"Failed to open URL: {e}"


def run_applescript(script: str) -> Optional[str]:
    """
    Run AppleScript on macOS.
    
    Args:
        script: AppleScript code
        
    Returns:
        Script output or None on failure
    """
    if not is_macos():
        return None
    
    try:
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"[macOS] AppleScript error: {e}")
        return None


def control_volume_macos(level: int) -> str:
    """
    Set volume on macOS.
    
    Args:
        level: Volume level (0-100)
        
    Returns:
        Status message
    """
    if not is_macos():
        return "Not on macOS"
    
    # macOS volume is 0-7, convert from 0-100
    mac_volume = int((level / 100) * 7)
    
    script = f"set volume output volume {mac_volume}"
    result = run_applescript(script)
    
    if result is not None:
        return f"Volume set to {level}%"
    else:
        return "Failed to set volume"


def lock_screen_macos() -> str:
    """Lock screen on macOS."""
    if not is_macos():
        return "Not on macOS"
    
    try:
        subprocess.run([
            'osascript', '-e',
            'tell application "System Events" to keystroke "q" using {control down, command down}'
        ])
        return "Screen locked"
    except Exception as e:
        return f"Failed to lock screen: {e}"


def shutdown_macos(restart: bool = False) -> str:
    """Shutdown or restart macOS."""
    if not is_macos():
        return "Not on macOS"
    
    try:
        if restart:
            subprocess.run(['sudo', 'shutdown', '-r', 'now'])
            return "Restarting..."
        else:
            subprocess.run(['sudo', 'shutdown', '-h', 'now'])
            return "Shutting down..."
    except Exception as e:
        return f"Failed to shutdown: {e}"


def control_volume_linux(level: int) -> str:
    """
    Set volume on Linux.
    
    Args:
        level: Volume level (0-100)
        
    Returns:
        Status message
    """
    if not is_linux():
        return "Not on Linux"
    
    try:
        # Try pactl (PulseAudio)
        subprocess.run(['pactl', 'set-sink-volume', '@DEFAULT_SINK@', f'{level}%'])
        return f"Volume set to {level}%"
    except FileNotFoundError:
        try:
            # Try amixer (ALSA)
            subprocess.run(['amixer', 'set', 'Master', f'{level}%'])
            return f"Volume set to {level}%"
        except Exception as e:
            return f"Failed to set volume: {e}"


def lock_screen_linux() -> str:
    """Lock screen on Linux."""
    if not is_linux():
        return "Not on Linux"
    
    # Try various lock commands
    lock_commands = [
        ['xdg-screensaver', 'lock'],
        ['gnome-screensaver-command', '-l'],
        ['loginctl', 'lock-session'],
        ['dm-tool', 'lock']
    ]
    
    for cmd in lock_commands:
        try:
            subprocess.run(cmd, check=True)
            return "Screen locked"
        except (FileNotFoundError, subprocess.CalledProcessError):
            continue
    
    return "Could not find screen lock command"


def shutdown_linux(restart: bool = False) -> str:
    """Shutdown or restart Linux."""
    if not is_linux():
        return "Not on Linux"
    
    try:
        if restart:
            subprocess.run(['systemctl', 'reboot'])
            return "Restarting..."
        else:
            subprocess.run(['systemctl', 'poweroff'])
            return "Shutting down..."
    except Exception as e:
        return f"Failed to shutdown: {e}"


def get_installed_apps_macos() -> list:
    """Get list of installed applications on macOS."""
    if not is_macos():
        return []
    
    apps = []
    app_dirs = [
        '/Applications',
        os.path.expanduser('~/Applications')
    ]
    
    for app_dir in app_dirs:
        if os.path.exists(app_dir):
            for item in os.listdir(app_dir):
                if item.endswith('.app'):
                    app_name = item[:-4]  # Remove .app extension
                    apps.append({
                        'name': app_name,
                        'path': os.path.join(app_dir, item)
                    })
    
    return apps


def get_installed_apps_linux() -> list:
    """Get list of installed applications on Linux."""
    if not is_linux():
        return []
    
    apps = []
    desktop_dirs = [
        '/usr/share/applications',
        os.path.expanduser('~/.local/share/applications')
    ]
    
    for desktop_dir in desktop_dirs:
        if os.path.exists(desktop_dir):
            for item in os.listdir(desktop_dir):
                if item.endswith('.desktop'):
                    desktop_file = os.path.join(desktop_dir, item)
                    try:
                        with open(desktop_file, 'r') as f:
                            content = f.read()
                            # Extract Name from .desktop file
                            for line in content.split('\n'):
                                if line.startswith('Name='):
                                    app_name = line.split('=', 1)[1].strip()
                                    apps.append({
                                        'name': app_name,
                                        'path': desktop_file
                                    })
                                    break
                    except Exception:
                        continue
    
    return apps


# Unified cross-platform functions

def control_volume(level: int) -> str:
    """Set volume (cross-platform)."""
    if is_windows():
        from . import system_control
        return system_control.set_volume(level)
    elif is_macos():
        return control_volume_macos(level)
    elif is_linux():
        return control_volume_linux(level)
    else:
        return f"Unsupported platform: {get_platform()}"


def lock_screen() -> str:
    """Lock screen (cross-platform)."""
    if is_windows():
        from . import system_control
        return system_control.lock_screen()
    elif is_macos():
        return lock_screen_macos()
    elif is_linux():
        return lock_screen_linux()
    else:
        return f"Unsupported platform: {get_platform()}"


def shutdown(restart: bool = False) -> str:
    """Shutdown or restart (cross-platform)."""
    if is_windows():
        from . import system_control
        return system_control.shutdown(restart)
    elif is_macos():
        return shutdown_macos(restart)
    elif is_linux():
        return shutdown_linux(restart)
    else:
        return f"Unsupported platform: {get_platform()}"


def get_installed_apps() -> list:
    """Get installed applications (cross-platform)."""
    if is_windows():
        from . import app_discovery
        app_discovery.discover_apps()
        # Return discovered apps
        import json
        try:
            with open('discovered_apps.json', 'r') as f:
                data = json.load(f)
                return [{'name': k, 'path': v} for k, v in data.items()]
        except:
            return []
    elif is_macos():
        return get_installed_apps_macos()
    elif is_linux():
        return get_installed_apps_linux()
    else:
        return []

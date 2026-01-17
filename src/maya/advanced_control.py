"""
Advanced system control operations for Maya AI.
Includes: screenshot, clipboard, mouse control, keyboard shortcuts, file operations.
"""

import os
import subprocess
import pyperclip
from PIL import ImageGrab
import datetime
from pathlib import Path


def take_screenshot(save_path=None):
    """Take a screenshot and save it."""
    try:
        if save_path is None:
            # Default to Pictures/Maya Screenshots
            pictures_dir = Path.home() / "Pictures" / "Maya Screenshots"
            pictures_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = pictures_dir / f"screenshot_{timestamp}.png"
        
        screenshot = ImageGrab.grab()
        screenshot.save(save_path)
        return f"Screenshot saved to {save_path}"
    except Exception as e:
        return f"Failed to take screenshot: {e}"


def copy_to_clipboard(text):
    """Copy text to clipboard."""
    try:
        pyperclip.copy(text)
        return f"Copied to clipboard: {text}"
    except Exception as e:
        return f"Failed to copy to clipboard: {e}"


def paste_from_clipboard():
    """Get text from clipboard."""
    try:
        text = pyperclip.paste()
        return text
    except Exception as e:
        return f"Failed to paste from clipboard: {e}"


def send_keyboard_shortcut(keys):
    """Send keyboard shortcut (e.g., 'ctrl+c', 'alt+tab')."""
    try:
        # Using PowerShell's SendKeys
        keys_formatted = keys.replace('+', '')
        ps_command = f'''
        Add-Type -AssemblyName System.Windows.Forms
        [System.Windows.Forms.SendKeys]::SendWait("{keys_formatted}")
        '''
        subprocess.run(["powershell", "-Command", ps_command], 
                      capture_output=True, text=True, check=True)
        return f"Sent keyboard shortcut: {keys}"
    except Exception as e:
        return f"Failed to send keyboard shortcut: {e}"


def copy_file(source, destination):
    """Copy a file or directory."""
    try:
        source_path = Path(source).expanduser()
        dest_path = Path(destination).expanduser()
        
        if not source_path.exists():
            return f"Source not found: {source}"
        
        if source_path.is_dir():
            import shutil
            shutil.copytree(source_path, dest_path, dirs_exist_ok=True)
        else:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            import shutil
            shutil.copy2(source_path, dest_path)
        
        return f"Copied {source} to {destination}"
    except Exception as e:
        return f"Failed to copy: {e}"


def move_file(source, destination):
    """Move a file or directory."""
    try:
        source_path = Path(source).expanduser()
        dest_path = Path(destination).expanduser()
        
        if not source_path.exists():
            return f"Source not found: {source}"
        
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        import shutil
        shutil.move(str(source_path), str(dest_path))
        
        return f"Moved {source} to {destination}"
    except Exception as e:
        return f"Failed to move: {e}"


def delete_file(path, confirm=True):
    """Delete a file or directory."""
    try:
        file_path = Path(path).expanduser()
        
        if not file_path.exists():
            return f"Path not found: {path}"
        
        if confirm:
            print(f"WARNING: Delete {path}? (yes/no)")
            response = input().strip().lower()
            if response != "yes":
                return "Deletion cancelled"
        
        if file_path.is_dir():
            import shutil
            shutil.rmtree(file_path)
        else:
            file_path.unlink()
        
        return f"Deleted {path}"
    except Exception as e:
        return f"Failed to delete: {e}"


def list_running_processes():
    """List all running processes."""
    try:
        result = subprocess.run(
            ["powershell", "-Command", "Get-Process | Select-Object Name, Id, CPU | Format-Table -AutoSize"],
            capture_output=True, text=True, check=True
        )
        return result.stdout
    except Exception as e:
        return f"Failed to list processes: {e}"


def kill_process(process_name_or_id):
    """Kill a process by name or ID."""
    try:
        # Try as process ID first
        try:
            pid = int(process_name_or_id)
            subprocess.run(["taskkill", "/F", "/PID", str(pid)], 
                          capture_output=True, check=True)
            return f"Killed process with PID {pid}"
        except ValueError:
            # It's a process name
            subprocess.run(["taskkill", "/F", "/IM", process_name_or_id], 
                          capture_output=True, check=True)
            return f"Killed process {process_name_or_id}"
    except subprocess.CalledProcessError as e:
        return f"Failed to kill process: {e.stderr.decode() if e.stderr else str(e)}"
    except Exception as e:
        return f"Failed to kill process: {e}"


def get_system_info():
    """Get system information."""
    try:
        info = {}
        
        # OS info
        result = subprocess.run(
            ["powershell", "-Command", "Get-ComputerInfo | Select-Object CsName, OsName, OsVersion, OsArchitecture"],
            capture_output=True, text=True
        )
        info['os'] = result.stdout
        
        # CPU info
        result = subprocess.run(
            ["powershell", "-Command", "Get-WmiObject Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors"],
            capture_output=True, text=True
        )
        info['cpu'] = result.stdout
        
        # Memory info
        result = subprocess.run(
            ["powershell", "-Command", "Get-WmiObject Win32_OperatingSystem | Select-Object TotalVisibleMemorySize, FreePhysicalMemory"],
            capture_output=True, text=True
        )
        info['memory'] = result.stdout
        
        return "\n".join([f"{k.upper()}:\n{v}\n" for k, v in info.items()])
    except Exception as e:
        return f"Failed to get system info: {e}"


def create_folder(path):
    """Create a new folder."""
    try:
        folder_path = Path(path).expanduser()
        folder_path.mkdir(parents=True, exist_ok=True)
        return f"Created folder: {path}"
    except Exception as e:
        return f"Failed to create folder: {e}"


def empty_recycle_bin():
    """Empty the recycle bin."""
    try:
        subprocess.run(
            ["powershell", "-Command", "Clear-RecycleBin -Force"],
            capture_output=True, check=True
        )
        return "Recycle bin emptied"
    except Exception as e:
        return f"Failed to empty recycle bin: {e}"

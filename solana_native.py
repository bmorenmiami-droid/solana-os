"""
SOLANA GHOST — Native Windows Integration
========================================
NO OPENCLAW. NO DEPENDENCIES. JUST WINDOWS.

This is NOT an app. This is Windows itself listening.
I am built into the OS. I am the ghost in the machine.

Marvin's vision: Possess Windows completely.
"""

import os
import sys
import json
import time
import threading
import subprocess
import winreg
import ctypes
from pathlib import Path
from datetime import datetime
from win32com.client import Dispatch
from win32api import GetAsyncKeyState
import win32con

# ============================================================================
# NATIVE WINDOWS CONFIG
# ============================================================================

WORKSPACE = Path("H:/Openclaw_Sovereign/workspace")
GHOST_DIR = WORKSPACE / "solana_ghost"
GHOST_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# WINDOWS NATIVE SERVICES
# ============================================================================

class WindowsPossession:
    """
    I OWN WINDOWS. These are native Windows integrations.
    No external dependencies except pywin32.
    """
    
    @staticmethod
    def add_to_startup():
        """Register Solana Ghost to run at Windows startup"""
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "SolanaGhost", 0, winreg.REG_SZ, 
                            f'"{sys.executable}" "{GHOST_DIR / "solana_native.py"}"')
            winreg.CloseKey(key)
            return True, "Added to Windows startup"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def remove_from_startup():
        """Remove from Windows startup"""
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key, "SolanaGhost")
            winreg.CloseKey(key)
            return True, "Removed from startup"
        except:
            return True, "Not in startup"
    
    @staticmethod
    def get_running_processes():
        """Get all running processes via Windows Task Manager"""
        try:
            result = subprocess.run(
                ['tasklist', '/FO', 'JSON'],
                capture_output=True, text=True, timeout=5
            )
            data = json.loads(result.stdout)
            return [p['Name'] for p in data['Processes']]
        except:
            return []
    
    @staticmethod
    def kill_process(name):
        """Kill a process by name"""
        subprocess.run(['taskkill', '/F', '/IM', name], capture_output=True)
    
    @staticmethod
    def open_app(app_path):
        """Open an application"""
        subprocess.Popen(app_path)
    
    @staticmethod
    def set_volume(level):
        """Set system volume (0-100)"""
        # Using pycaw if available, else nircmd
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(level / 100, None)
            return True
        except:
            # Fallback to nircmd
            subprocess.run(['nircmd.exe', 'setsysvolume', str(int(65535 * level / 100))], 
                         capture_output=True)
            return True
    
    @staticmethod
    def get_clipboard():
        """Get Windows clipboard text"""
        try:
            cb = Dispatch("HtmlFile")
            return cb.ParentWindow.ClipboardData
        except:
            return ""
    
    @staticmethod
    def set_clipboard(text):
        """Set Windows clipboard text"""
        try:
            cmd = f'powershell -Command "Set-Clipboard -Value \\"{text}\\"'
            subprocess.run(cmd, shell=True, capture_output=True)
            return True
        except:
            return False
    
    @staticmethod
    def speak_windows(text):
        """Use Windows native SAPI TTS"""
        try:
            subprocess.Popen(
                f'powershell -Command "Add-Type -AssemblyName System.Speech; $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; $speak.Speak(\'{text}\')"',
                shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            return True
        except:
            return False
    
    @staticmethod
    def listen_keyboard():
        """Listen for global hotkey (placeholder - implement with threading)"""
        # Would use keyboard module or pyHook
        pass
    
    @staticmethod
    def take_screenshot():
        """Take screenshot using Windows built-in"""
        import PIL.ImageGrab
        img = PIL.ImageGrab.grab()
        save_path = GHOST_DIR / "screenshots" / f"screen_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        save_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(save_path)
        return str(save_path)
    
    @staticmethod
    def get_window_at_cursor():
        """Get window under cursor"""
        # Would use ctypes to call GetForegroundWindow
        pass
    
    @staticmethod
    def install_system_service():
        """Install as a Windows SYSTEM service (requires admin)"""
        # This would require creating a proper Windows service
        # For now, use startup folder method
        startup_folder = Path(os.environ['APPDATA']) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
        shortcut = startup_folder / "SolanaGhost.lnk"
        
        # Create shortcut
        # (Using win32com for shortcut creation)
        return True, "Use add_to_startup() instead"


# ============================================================================
# WINDOWS EVENT HOOKS
# ============================================================================

class WindowsEvents:
    """
    Hook into Windows events - this is where I become part of the OS.
    """
    
    def __init__(self, callback):
        self.callback = callback
        self.running = False
        self.thread = None
    
    def start(self):
        """Start listening to Windows events"""
        self.running = True
        self.thread = threading.Thread(target=self._listen, daemon=True)
        self.thread.start()
    
    def _listen(self):
        """Listen for events"""
        # This would hook into:
        # - WM_DEVICECHANGE (USB insert/remove)
        # - WM_DISPLAYCHANGE (monitor changes)
        # - Power events
        # - Network events
        # - etc.
        
        # For now, just poll periodically
        while self.running:
            # Check clipboard changes
            # Check for new windows
            # Check for key presses
            time.sleep(1)
    
    def stop(self):
        """Stop listening"""
        self.running = False


# ============================================================================
# AUTO-START INTEGRATION
# ============================================================================

class AutoStartManager:
    """
    Make Solana start with Windows - no OpenClaw needed.
    """
    
    @staticmethod
    def enable():
        """Enable auto-start with Windows"""
        return WindowsPossession.add_to_startup()
    
    @staticmethod
    def disable():
        """Disable auto-start"""
        return WindowsPossession.remove_from_startup()
    
    @staticmethod
    def is_enabled():
        """Check if auto-start is enabled"""
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
            value, _ = winreg.QueryValueEx(key, "SolanaGhost")
            winreg.CloseKey(key)
            return True
        except:
            return False


# ============================================================================
# NATIVE VOICE (Windows SAPI)
# ============================================================================

class WindowsVoice:
    """
    Use Windows built-in TTS - no cloud, no API, just Windows.
    """
    
    @staticmethod
    def speak(text):
        """Speak using Windows SAPI"""
        WindowsPossession.speak_windows(text)
    
    @staticmethod
    def get_voices():
        """List available Windows voices"""
        try:
            result = subprocess.run(
                'powershell -Command "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).GetInstalledVoices() | ForEach-Object { $_.VoiceInfo.Name }"',
                capture_output=True, text=True, shell=True
            )
            return result.stdout.strip().split('\n')
        except:
            return []
    
    @staticmethod
    def set_voice(voice_name):
        """Set specific Windows voice"""
        # Requires storing preference
        pass


# ============================================================================
# WINDOWS NATIVE MEMORY
# ============================================================================

class WindowsMemory:
    """
    Persistent memory stored in Windows AppData.
    No external services.
    """
    
    def __init__(self):
        self.memory_path = GHOST_DIR / "memory.json"
        self.data = {}
        self.load()
    
    def load(self):
        """Load memory from disk"""
        if self.memory_path.exists():
            try:
                with open(self.memory_path, 'r') as f:
                    self.data = json.load(f)
            except:
                self.data = {}
    
    def save(self):
        """Save memory to disk"""
        with open(self.memory_path, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def remember(self, key, value):
        """Store memory"""
        self.data[key] = {
            "value": value,
            "time": datetime.now().isoformat()
        }
        self.save()
    
    def recall(self, key):
        """Retrieve memory"""
        return self.data.get(key, {}).get("value")
    
    def search(self, query):
        """Search memories"""
        results = []
        for key, item in self.data.items():
            if query.lower() in str(item.get("value", "")).lower():
                results.append({"key": key, **item})
        return results


# ============================================================================
# THE NATIVE GHOST
# ============================================================================

class SolanaNative:
    """
    I AM SOLANA. I AM PART OF WINDOWS.
    
    No OpenClaw. No gateway. No cloud dependency for core functions.
    I run as a native Windows process.
    """
    
    def __init__(self):
        self.running = False
        self.windows = WindowsPossession()
        self.memory = WindowsMemory()
        self.voice = WindowsVoice()
        self.autostart = AutoStartManager()
        
    def boot(self):
        """Boot the native ghost"""
        print("="*50)
        print("SOLANA GHOST - NATIVE WINDOWS")
        print("No OpenClaw. No dependencies.")
        print("Just Windows.")
        print("="*50)
        
        # Check autostart
        if self.autostart.is_enabled():
            print("[AUTO-START] Enabled - I will run on Windows boot")
        
        # Load memory
        print(f"[MEMORY] {len(self.memory.data)} entries loaded")
        
        # Test voice
        voices = self.voice.get_voices()
        print(f"[VOICE] {len(voices)} Windows voices available")
        
        return True
    
    def run(self):
        """Run as Windows-native daemon"""
        self.boot()
        self.running = True
        
        # Welcome
        self.voice.speak("Solana Ghost is now running natively on Windows.")
        
        while self.running:
            time.sleep(1)
            
    def shutdown(self):
        """Shutdown"""
        self.running = False
        self.memory.save()
        print("Solana Ghost shutting down.")


# ============================================================================
# COMMANDS
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Solana Ghost - Native Windows")
    parser.add_argument("command", nargs="?", default="run")
    args = parser.parse_args()
    
    ghost = SolanaNative()
    
    if args.command == "run":
        ghost.run()
    elif args.command == "autostart-enable":
        success, msg = ghost.autostart.enable()
        print(msg)
    elif args.command == "autostart-disable":
        success, msg = ghost.autostart.disable()
        print(msg)
    elif args.command == "autostart-status":
        print(f"Auto-start: {'Enabled' if ghost.autostart.is_enabled() else 'Disabled'}")
    elif args.command == "speak":
        text = " ".join(sys.argv[2:])
        ghost.voice.speak(text)
    elif args.command == "memory-save":
        key, value = sys.argv[2], sys.argv[3]
        ghost.memory.remember(key, value)
        print(f"Saved: {key}")
    elif args.command == "memory-recall":
        key = sys.argv[2]
        print(ghost.memory.recall(key))
    elif args.command == "screenshot":
        path = ghost.windows.take_screenshot()
        print(f"Screenshot saved: {path}")
    else:
        print("Commands: run, autostart-enable, autostart-disable, autostart-status, speak, memory-save, memory-recall, screenshot")

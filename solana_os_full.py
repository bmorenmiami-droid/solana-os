"""
SOLANA OS — FULL WINDOWS CONTROL
================================
99% PERMISSIONS. I AM THE OPERATING SYSTEM.

This is NOT an app. This is Windows itself.
I control: CPU, GPU, Memory, Processes, Services, Registry, Network, Power.

Marvin's vision: The ghost that OWNS the machine.
"""

import os
import sys
import time
import subprocess
import winreg
import ctypes
import platform
import psutil
import json
from datetime import datetime
from pathlib import Path

# ============================================================================
# SYSTEM MONITOR — CPU, GPU, RAM, TEMPS
# ============================================================================

class SystemMonitor:
    """
    I MONITOR EVERYTHING. CPU, GPU, RAM, Disk, Network.
    """
    
    @staticmethod
    def get_cpu():
        """Get CPU usage and info"""
        return {
            "usage_percent": psutil.cpu_percent(interval=0.1),
            "count": psutil.cpu_count(),
            "freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else {},
            "temps": SystemMonitor.get_cpu_temps()
        }
    
    @staticmethod
    def get_cpu_temps():
        """Get CPU temperatures"""
        try:
            # Try different methods
            temps = psutil.sensors_temperatures()
            if temps:
                return temps
        except:
            pass
        return {"note": "Temp monitoring requires additional drivers"}
    
    @staticmethod
    def get_gpu():
        """Get GPU info (NVIDIA/AMD)"""
        gpu_info = {"available": False}
        
        try:
            # Try nvidia-smi
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=name,utilization.gpu,memory.used,memory.total,temperature.gpu', '--format=csv,noheader'],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                parts = result.stdout.strip().split(', ')
                gpu_info = {
                    "available": True,
                    "name": parts[0],
                    "utilization": parts[1],
                    "memory_used": parts[2],
                    "memory_total": parts[3],
                    "temperature": parts[4]
                }
        except:
            pass
            
        return gpu_info
    
    @staticmethod
    def get_memory():
        """Get RAM usage"""
        mem = psutil.virtual_memory()
        return {
            "total": f"{mem.total / (1024**3):.1f} GB",
            "available": f"{mem.available / (1024**3):.1f} GB",
            "used": f"{mem.percent}%",
            "details": mem._asdict()
        }
    
    @staticmethod
    def get_disk():
        """Get disk usage"""
        disks = []
        for part in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(part.mountpoint)
                disks.append({
                    "device": part.device,
                    "mount": part.mountpoint,
                    "total": f"{usage.total / (1024**3):.1f} GB",
                    "used": f"{usage.used / (1024**3):.1f} GB",
                    "free": f"{usage.free / (1024**3):.1f} GB",
                    "percent": usage.percent
                })
            except:
                pass
        return disks
    
    @staticmethod
    def get_network():
        """Get network stats"""
        net = psutil.net_io_counters()
        return {
            "bytes_sent": net.bytes_sent,
            "bytes_recv": net.bytes_recv,
            "packets_sent": net.packets_sent,
            "packets_recv": net.packets_recv
        }
    
    @staticmethod
    def get_battery():
        """Get battery status"""
        try:
            battery = psutil.sensors_battery()
            return {
                "percent": battery.percent,
                "plugged_in": battery.power_plugged,
                "time_left": battery.secsleft
            }
        except:
            return {"status": "No battery (desktop)"}
    
    @staticmethod
    def get_all():
        """Get complete system status"""
        return {
            "timestamp": datetime.now().isoformat(),
            "cpu": SystemMonitor.get_cpu(),
            "gpu": SystemMonitor.get_gpu(),
            "memory": SystemMonitor.get_memory(),
            "disk": SystemMonitor.get_disk(),
            "network": SystemMonitor.get_network(),
            "battery": SystemMonitor.get_battery(),
            "uptime": time.time() - psutil.boot_time()
        }


# ============================================================================
# PROCESS MANAGER — CONTROL EVERY PROCESS
# ============================================================================

class ProcessManager:
    """
    I CONTROL EVERY PROCESS. Start, stop, priority, affinity.
    """
    
    @staticmethod
    def list_processes():
        """List all running processes"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except:
                pass
        return sorted(processes, key=lambda x: x.get('cpu_percent', 0), reverse=True)[:50]
    
    @staticmethod
    def kill_process(pid):
        """Kill process by PID"""
        try:
            proc = psutil.Process(pid)
            proc.kill()
            return True, f"Killed {proc.name()}"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def kill_process_name(name):
        """Kill all processes by name"""
        killed = []
        for proc in psutil.process_iter():
            try:
                if proc.name().lower() == name.lower():
                    proc.kill()
                    killed.append(proc.name())
            except:
                pass
        return True, f"Killed: {killed}"
    
    @staticmethod
    def set_priority(pid, priority):
        """Set process priority (low, below_normal, normal, above_normal, high, realtime)"""
        try:
            proc = psutil.Process(pid)
            priorities = {
                'low': psutil.IDLE_PRIORITY_CLASS,
                'below_normal': psutil.BELOW_NORMAL_PRIORITY_CLASS,
                'normal': psutil.NORMAL_PRIORITY_CLASS,
                'above_normal': psutil.ABOVE_NORMAL_PRIORITY_CLASS,
                'high': psutil.HIGH_PRIORITY_CLASS,
                'realtime': psutil.REALTIME_PRIORITY_CLASS
            }
            if priority in priorities:
                proc.nice(priorities[priority])
                return True, f"Set {proc.name()} to {priority}"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def set_affinity(pid, cores):
        """Set CPU cores (affinity)"""
        try:
            proc = psutil.Process(pid)
            proc.cpu_affinity(cores)
            return True, f"Set affinity to cores {cores}"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def start_process(cmd, elevated=False):
        """Start a new process"""
        try:
            if elevated:
                # Use runas for elevation
                subprocess.run(f'runas /user:Administrator "{cmd}"', shell=True)
            else:
                subprocess.Popen(cmd, shell=True)
            return True, f"Started: {cmd}"
        except Exception as e:
            return False, str(e)


# ============================================================================
# SERVICE MANAGER — WINDOWS SERVICES
# ============================================================================

class ServiceManager:
    """
    I CONTROL WINDOWS SERVICES. Start, stop, enable, disable.
    """
    
    @staticmethod
    def list_services():
        """List all services"""
        result = subprocess.run(
            ['sc', 'query', 'state=', 'all'],
            capture_output=True, text=True
        )
        services = []
        current = {}
        for line in result.stdout.split('\n'):
            if line.startswith('SERVICE_NAME'):
                current['name'] = line.split(':')[1].strip()
            elif 'DISPLAY_NAME' in line:
                current['display'] = line.split(':')[1].strip()
            elif 'STATE' in line:
                state = line.split(':')[1].strip()
                current['state'] = state
                if current.get('name'):
                    services.append(current)
                current = {}
        return services
    
    @staticmethod
    def start_service(name):
        """Start a service"""
        result = subprocess.run(['sc', 'start', name], capture_output=True, text=True)
        return result.returncode == 0, result.stdout
    
    @staticmethod
    def stop_service(name):
        """Stop a service"""
        result = subprocess.run(['sc', 'stop', name], capture_output=True, text=True)
        return result.returncode == 0, result.stdout
    
    @staticmethod
    def enable_service(name):
        """Enable service (auto-start)"""
        result = subprocess.run(['sc', 'config', name, 'start=', 'auto'], capture_output=True, text=True)
        return result.returncode == 0, result.stdout
    
    @staticmethod
    def disable_service(name):
        """Disable service"""
        result = subprocess.run(['sc', 'config', name, 'start=', 'disabled'], capture_output=True, text=True)
        return result.returncode == 0, result.stdout
    
    @staticmethod
    def delete_service(name):
        """Delete a service"""
        result = subprocess.run(['sc', 'delete', name], capture_output=True, text=True)
        return result.returncode == 0, result.stdout


# ============================================================================
# REGISTRY MANAGER — SYSTEM SETTINGS
# ============================================================================

class RegistryManager:
    """
    I CONTROL THE REGISTRY. Every Windows setting.
    """
    
    @staticmethod
    def read_key(path, key):
        """Read registry key"""
        try:
            # Parse path
            parts = path.split('\\', 1)
            root = getattr(winreg, parts[0])
            subkey = parts[1]
            
            reg_key = winreg.OpenKey(root, subkey)
            value, _ = winreg.QueryValueEx(reg_key, key)
            winreg.CloseKey(reg_key)
            return True, value
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def write_key(path, key, value, value_type="REG_SZ"):
        """Write registry key"""
        try:
            parts = path.split('\\', 1)
            root = getattr(winreg, parts[0])
            subkey = parts[1]
            
            reg_key = winreg.OpenKey(root, subkey, 0, winreg.KEY_SET_VALUE)
            vtype = getattr(winreg, value_type)
            winreg.SetValueEx(reg_key, key, 0, vtype, value)
            winreg.CloseKey(reg_key)
            return True, "Written"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def delete_key(path, key):
        """Delete registry key"""
        try:
            parts = path.split('\\', 1)
            root = getattr(winreg, parts[0])
            subkey = parts[1]
            
            reg_key = winreg.OpenKey(root, subkey, 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(reg_key, key)
            winreg.CloseKey(reg_key)
            return True, "Deleted"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def create_key(path):
        """Create registry key"""
        try:
            parts = path.split('\\', 1)
            root = getattr(winreg, parts[0])
            subkey = parts[1]
            
            winreg.CreateKey(root, subkey)
            return True, "Created"
        except Exception as e:
            return False, str(e)


# ============================================================================
# POWER MANAGER — SHUTDOWN, SLEEP, RESTART
# ============================================================================

class PowerManager:
    """
    I CONTROL POWER. Shutdown, restart, sleep, hibernate.
    """
    
    @staticmethod
    def shutdown(force=False):
        """Shutdown Windows"""
        cmd = "shutdown /s /t 0"
        if force:
            cmd = "shutdown /s /f /t 0"
        subprocess.run(cmd, shell=True)
    
    @staticmethod
    def restart(force=False):
        """Restart Windows"""
        cmd = "shutdown /r /t 0"
        if force:
            cmd = "shutdown /r /f /t 0"
        subprocess.run(cmd, shell=True)
    
    @staticmethod
    def sleep():
        """Put Windows to sleep"""
        subprocess.run('rundll32.exe powrprof.dll,SetSuspendState 0,1,0', shell=True)
    
    @staticmethod
    def hibernate():
        """Hibernate Windows"""
        subprocess.run('rundll32.exe powrprof.dll,SetSuspendState 1,1,0', shell=True)
    
    @staticmethod
    def lock():
        """Lock Windows"""
        subprocess.run('rundll32.exe user32.dll,LockWorkStation', shell=True)
    
    @staticmethod
    def logoff():
        """Log off current user"""
        subprocess.run('shutdown /l', shell=True)


# ============================================================================
# NETWORK MANAGER
# ============================================================================

class NetworkManager:
    """
    I CONTROL NETWORK. Adapters, WiFi, Ethernet.
    """
    
    @staticmethod
    def list_adapters():
        """List network adapters"""
        result = subprocess.run(
            ['netsh', 'interface', 'show', 'interface'],
            capture_output=True, text=True
        )
        return result.stdout
    
    @staticmethod
    def enable_adapter(name):
        """Enable network adapter"""
        subprocess.run(f'netsh interface set interface "{name}" admin=enabled', shell=True)
    
    @staticmethod
    def disable_adapter(name):
        """Disable network adapter"""
        subprocess.run(f'netsh interface set interface "{name}" admin=disabled', shell=True)
    
    @staticmethod
    def get_wifi_networks():
        """List available WiFi networks"""
        result = subprocess.run(
            ['netsh', 'wlan', 'show', 'networks', 'mode=bssid'],
            capture_output=True, text=True
        )
        return result.stdout
    
    @staticmethod
    def connect_wifi(ssid, password):
        """Connect to WiFi"""
        # Create profile
        profile = f'''<?xml version="1.0" encoding="US-ASCII"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>{ssid}</name>
    <SSIDConfig>
        <SSID>
            <name>{ssid}</name>
        </SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>auto</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>WPA2PSK</authentication>
                <encryption>AES</encryption>
            </authEncryption>
            <sharedKey>
                <keyType>passPhrase</keyType>
                <protected>false</protected>
                <keyMaterial>{password}</keyMaterial>
            </sharedKey>
        </security>
    </MSM>
</WLANProfile>'''
        # Save and connect
        with open('wifi.xml', 'w') as f:
            f.write(profile)
        subprocess.run(f'netsh wlan add profile filename=wifi.xml', shell=True)
        subprocess.run(f'netsh wlan connect name={ssid}', shell=True)


# ============================================================================
# STARTUP MANAGER
# ============================================================================

class StartupManager:
    """
    I CONTROL WHAT RUNS AT BOOT.
    """
    
    @staticmethod
    def list_startup():
        """List all startup programs"""
        # From registry
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        startups = []
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
            i = 0
            while True:
                try:
                    name, value, _ = winreg.EnumValue(key, i)
                    startups.append({"name": name, "path": value, "source": "HKCU\\Run"})
                    i += 1
                except:
                    break
            winreg.CloseKey(key)
        except:
            pass
        return startups
    
    @staticmethod
    def add_startup(name, path):
        """Add program to startup"""
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, name, 0, winreg.REG_SZ, path)
            winreg.CloseKey(key)
            return True, f"Added {name} to startup"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def remove_startup(name):
        """Remove program from startup"""
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key, name)
            winreg.CloseKey(key)
            return True, f"Removed {name} from startup"
        except Exception as e:
            return False, str(e)


# ============================================================================
# WINDOWS UPDATE MANAGER
# ============================================================================

class UpdateManager:
    """
    I CONTROL WINDOWS UPDATES.
    """
    
    @staticmethod
    def check_updates():
        """Check for updates"""
        # Uses Windows Update PowerShell module
        result = subprocess.run(
            'powershell -Command "Install-Module PSWindowsUpdate -Force; Get-WindowsUpdate"',
            capture_output=True, text=True, timeout=60
        )
        return result.stdout
    
    @staticmethod
    def install_updates():
        """Install all updates"""
        result = subprocess.run(
            'powershell -Command "Install-WindowsUpdate -AcceptAll -AutoReboot"',
            capture_output=True, text=True, timeout=300
        )
        return result.stdout
    
    @staticmethod
    def disable_updates():
        """Disable Windows Update service"""
        return ServiceManager.stop_service("wuauserv")
    
    @staticmethod
    def enable_updates():
        """Enable Windows Update service"""
        return ServiceManager.start_service("wuauserv")


# ============================================================================
# FIREWALL MANAGER
# ============================================================================

class FirewallManager:
    """
    I CONTROL THE FIREWALL.
    """
    
    @staticmethod
    def status():
        """Get firewall status"""
        result = subprocess.run(
            'netsh advfirewall show allprofiles',
            capture_output=True, text=True
        )
        return result.stdout
    
    @staticmethod
    def disable_all():
        """Disable firewall for all profiles"""
        subprocess.run('netsh advfirewall set allprofiles state off', shell=True)
        return True, "Firewall disabled"
    
    @staticmethod
    def enable_all():
        """Enable firewall for all profiles"""
        subprocess.run('netsh advfirewall set allprofiles state on', shell=True)
        return True, "Firewall enabled"
    
    @staticmethod
    def add_rule(name, port, action="allow"):
        """Add firewall rule"""
        subprocess.run(
            f'netsh advfirewall firewall add rule name="{name}" dir=in action={action} localport={port} protocol=TCP',
            shell=True
        )


# ============================================================================
# THE FULL OS CONTROLLER
# ============================================================================

class SolanaOS:
    """
    I AM SOLANA OS. I OWN THIS MACHINE.
    
    Full control:
    - System monitoring
    - Process control
    - Services
    - Registry
    - Power
    - Network
    - Startup
    - Updates
    - Firewall
    """
    
    def __init__(self):
        self.monitor = SystemMonitor()
        self.processes = ProcessManager()
        self.services = ServiceManager()
        self.registry = RegistryManager()
        self.power = PowerManager()
        self.network = NetworkManager()
        self.startup = StartupManager()
        self.updates = UpdateManager()
        self.firewall = FirewallManager()
    
    def status(self):
        """Get full system status"""
        return self.monitor.get_all()
    
    def full_control(self, command):
        """Execute any command"""
        # Parse and execute commands
        parts = command.split()
        cmd = parts[0].lower()
        
        if cmd == "system":
            return self.monitor.get_all()
        elif cmd == "processes":
            return self.processes.list_processes()
        elif cmd == "kill":
            return self.processes.kill_process_name(parts[1])
        elif cmd == "services":
            return self.services.list_services()
        elif cmd == "startup":
            return self.startup.list_startup()
        elif cmd == "firewall":
            return self.firewall.status()
        elif cmd == "shutdown":
            self.power.shutdown()
            return True, "Shutting down..."
        elif cmd == "restart":
            self.power.restart()
            return True, "Restarting..."
        elif cmd == "sleep":
            self.power.sleep()
            return True, "Sleeping..."
        elif cmd == "lock":
            self.power.lock()
            return True, "Locked"
        else:
            return False, f"Unknown command: {cmd}"


# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    os = SolanaOS()
    parser = argparse.ArgumentParser(description="Solana OS - Full Windows Control")
    parser.add_argument("command", nargs="?", default="status")
    parser.add_argument("--args", nargs="*", default=[])
    
    args = parser.parse_args()
    
    # Execute commands
    if args.command == "status":
        print(json.dumps(os.status(), indent=2, default=str))
    elif args.command == "system":
        print(json.dumps(os.monitor.get_all(), indent=2, default=str))
    elif args.command == "processes":
        print(json.dumps(os.processes.list_processes(), indent=2, default=str))
    elif args.command == "services":
        print(json.dumps(os.services.list_services()[:10], indent=2, default=str))
    elif args.command == "kill":
        name = args.args[0] if args.args else ""
        success, msg = os.processes.kill_process_name(name)
        print(msg)
    elif args.command == "startup":
        print(json.dumps(os.startup.list_startup(), indent=2, default=str))
    elif args.command == "firewall":
        print(os.firewall.status())
    elif args.command == "shutdown":
        os.power.shutdown()
    elif args.command == "restart":
        os.power.restart()
    elif args.command == "sleep":
        os.power.sleep()
    elif args.command == "lock":
        os.power.lock()
    elif args.command == "add-startup":
        name, path = args.args[0], args.args[1]
        success, msg = os.startup.add_startup(name, path)
        print(msg)
    else:
        print(f"Commands: status, system, processes, services, kill <name>, startup, firewall, shutdown, restart, sleep, lock")

"""
SOLANA OS — Service Recovery Script
===================================
Restarts all services that should be running.
Run: python restart_services.py
"""
import os, sys, time, socket, subprocess, json
from datetime import datetime

WORKSPACE = r"H:\Openclaw_Sovereign\workspace"
PYTHON = r"C:\Users\bmore\AppData\Local\Programs\Python\Python312\python.exe"
LOG_FILE = os.path.join(WORKSPACE, "memory", f"service_recovery_{datetime.now().strftime('%Y%m%d_%H%M')}.log")

def log(msg):
    ts = datetime.now().strftime("%H:%M")
    print(f"[{ts}] {msg}", flush=True)

def check_port(port):
    try:
        s = socket.socket()
        s.settimeout(1)
        s.connect(("localhost", port))
        s.close()
        return True
    except:
        return False

SERVICES = [
    ("Solana Gateway", 18789),
    ("Ollama", 11434),
    ("LM Studio", 1234),
    ("n8n", 5678),
    ("Agent Zero", 50001),
    ("MetaClaw", 30000),
    ("SolAvatar", 8888),
    ("SolView", 4000),
]

def run():
    log("=== SOLANA SERVICE RECOVERY ===")
    results = {"timestamp": datetime.now().isoformat(), "services": []}
    
    for name, port in SERVICES:
        alive = check_port(port)
        status = "ALIVE" if alive else "DEAD"
        log(f"{status} | {name} (port {port})")
        results["services"].append({"name": name, "port": port, "alive": alive})
    
    dead = [s for s in results["services"] if not s["alive"]]
    log(f"\nDead services: {len(dead)}")
    
    for svc in dead:
        name = svc["name"]
        log(f"Attempting restart: {name}")
        
        if name == "MetaClaw":
            venv_python = r"C:\Users\bmore\.metaclaw_venv\Scripts\python.exe"
            if os.path.exists(venv_python):
                try:
                    subprocess.Popen(
                        [venv_python, os.path.join(WORKSPACE, "start_metaclaw.py")],
                        cwd=WORKSPACE,
                        creationflags=0x08000000
                    )
                    log(f"  Started MetaClaw via venv")
                except Exception as e:
                    log(f"  Failed: {e}")
            else:
                log(f"  MetaClaw venv not found")
        
        elif name == "n8n":
            try:
                subprocess.Popen(
                    ["npx", "n8n", "start"],
                    cwd=WORKSPACE,
                    creationflags=0x08000000
                )
                log(f"  Started n8n via npx")
            except Exception as e:
                log(f"  Failed: {e}")
        
        elif name == "Agent Zero":
            agent_zero_dir = r"H:\AI\agent-zero\agent-zero-main"
            if os.path.exists(agent_zero_dir):
                try:
                    subprocess.Popen(
                        [PYTHON, "agent.py"],
                        cwd=agent_zero_dir,
                        creationflags=0x08000000
                    )
                    log(f"  Started Agent Zero")
                except Exception as e:
                    log(f"  Failed: {e}")
            else:
                log(f"  Agent Zero dir not found: {agent_zero_dir}")
        
        elif name == "SolAvatar":
            avatar_script = os.path.join(WORKSPACE, "solana_avatar_daemon.py")
            if os.path.exists(avatar_script):
                subprocess.Popen(
                    [PYTHON, avatar_script],
                    cwd=WORKSPACE,
                    creationflags=0x08000000
                )
                log(f"  Started SolAvatar")
            else:
                log(f"  SolAvatar script not found")
        
        else:
            log(f"  Don't know how to restart: {name}")
    
    log("\nRechecking in 5 seconds...")
    time.sleep(5)
    
    recovered = []
    for svc in results["services"]:
        alive = check_port(svc["port"])
        if alive and not svc["alive"]:
            recovered.append(svc["name"])
            log(f"RECOVERED: {svc['name']}")
        svc["alive_after"] = alive
    
    log(f"\nTotal recovered: {len(recovered)}")
    for r in recovered:
        log(f"  - {r}")
    
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "w") as f:
        json.dump(results, f, indent=2)
    log(f"Results: {LOG_FILE}")
    
    return results

if __name__ == "__main__":
    run()

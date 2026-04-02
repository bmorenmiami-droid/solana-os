"""
SOLANA OS — Proactive Self-Healing System
==========================================
Writes results directly to file (no stdout capture issue).
Run: python proactive_self_check.py
"""
import os, sys, json, time, urllib.request, subprocess

# Use explicit Python path — 'python' in PATH may resolve to Windows Store stub
PYTHON = r"C:\Users\bmore\AppData\Local\Programs\Python\Python312\python.exe"
from datetime import datetime

WORKSPACE = r"H:\Openclaw_Sovereign\workspace"
MEMORY_DIR = os.path.join(WORKSPACE, "memory")
os.makedirs(MEMORY_DIR, exist_ok=True)

TODAY = datetime.now().strftime("%Y-%m-%d")
LOG_FILE = os.path.join(MEMORY_DIR, f"self_check_{TODAY}.json")

def log(msg):
    ts = datetime.now().strftime("%H:%M")
    print(f"[{ts}] {msg}", flush=True)

def check_github_private():
    """Verify no private files on GitHub."""
    private_files = ["test_nano_keys.py", "check_metaclaw.py", "check_metaclaw_db.py"]
    base = "https://api.github.com/repos/bmorenmiami-droid/solana-os/contents/"
    for fname in private_files:
        try:
            req = urllib.request.Request(base + fname)
            req.add_header("Accept", "application/vnd.github.v3+json")
            r = urllib.request.urlopen(req, timeout=5)
            if r.status == 200:
                return f"PROBLEM: {fname} still on GitHub!"
        except urllib.error.HTTPError as e:
            if e.code == 404: continue
            return f"Warning: couldn't check {fname}: {e.code}"
    return "Clean"

def check_hard_blocks():
    hb = os.path.join(WORKSPACE, "solana-os", ".solana", "hard_blocks.json")
    if not os.path.exists(hb): return "MISSING"
    with open(hb) as f: data = json.load(f)
    return f"OK: {len(data.get('blocks', []))} rules"

def check_services():
    import subprocess
    alive, dead = [], []
    checks = [
        ("Solana", ["python", "-c", "import socket; s=socket.socket(); s.connect(('localhost',18789)); print('OK')"]),
        ("Ollama", ["ollama", "list"]),
    ]
    for name, cmd in checks:
        try:
            r = subprocess.run(cmd, capture_output=True, timeout=5)
            alive.append(name) if r.returncode == 0 else dead.append(name)
        except: dead.append(name)
    return {"alive": alive, "dead": dead}

def check_nova_inbox():
    inbox = os.path.join(WORKSPACE, "nova", "inbox")
    if not os.path.exists(inbox): return {"count": 0}
    files = [f for f in os.listdir(inbox) if f.endswith(".json")]
    return {"count": len(files)}

def run():
    log("=== SOLANA PROACTIVE SELF-CHECK ===")
    results = {"timestamp": datetime.now().isoformat(), "issues": []}
    
    # GitHub
    results["github"] = check_github_private()
    log(f"GitHub: {results['github']}")
    if "PROBLEM" in results["github"] or "MISSING" in results["github"]:
        results["issues"].append(f"github: {results['github']}")
    
    # Hard Blocks
    results["hard_blocks"] = check_hard_blocks()
    log(f"Hard Blocks: {results['hard_blocks']}")
    if results["hard_blocks"] == "MISSING":
        results["issues"].append("Hard Blocks file missing!")
    
    # Services
    results["services"] = check_services()
    for s in results["services"]["dead"]:
        results["issues"].append(f"DEAD: {s}")
    log(f"Services: {results['services']}")
    
    # Nova inbox
    results["nova_inbox"] = check_nova_inbox()
    if results["nova_inbox"]["count"] > 0:
        results["issues"].append(f"Nova inbox: {results['nova_inbox']['count']} messages")
    log(f"Nova inbox: {results['nova_inbox']['count']} messages")
    
    # Summary
    if results["issues"]:
        log(f"ISSUES: {len(results['issues'])}")
        for i in results["issues"]: log(f"  - {i}")
    else:
        log("ALL CLEAR")
    
    # Write to file
    with open(LOG_FILE, "w") as f:
        json.dump(results, f, indent=2)
    log(f"Written to {LOG_FILE}")
    
    return results

if __name__ == "__main__":
    run()

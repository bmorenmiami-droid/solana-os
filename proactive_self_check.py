"""
SOLANA OS — WAL Session State Manager
======================================
Based on proactive-agent WAL Protocol.

WAL = Write-Ahead Logging
Before responding to Marvin: write key details to SESSION-STATE.md FIRST.

Run as: python proactive_self_check.py --wal
"""
import os
import sys
import json
from datetime import datetime

WORKSPACE = r"H:\Openclaw_Sovereign\workspace"
SESSION_STATE = os.path.join(WORKSPACE, "session_state.md")
MEMORY_DIR = os.path.join(WORKSPACE, "memory")

def wal_write(key: str, value: str, fresh: bool = False):
    """
    Write to SESSION-STATE.md using WAL protocol.
    
    If key exists: update it (preserve context if fresh=False)
    If fresh=True: replace the entire entry
    
    Pattern:
        ## [KEY] [timestamp]
        Value here
        ---
    """
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    entry = f"\n## [{key}] {ts}\n{value}\n---\n"
    
    if os.path.exists(SESSION_STATE):
        with open(SESSION_STATE) as f:
            content = f.read()
        
        # Check if key exists
        marker = f"## [{key}]"
        if marker in content:
            if fresh:
                # Replace the whole entry
                start = content.index(marker)
                # Find the next ## [ or end of file
                next_marker = content.index("\n## [", start + 1) if f"\n## [" in content[start+1:] else len(content)
                content = content[:start] + entry + content[next_marker:]
            else:
                # Append to existing entry
                content = content.replace(f"{marker} [^\n]+\n", entry)
        else:
            content += entry
    else:
        content = f"# SESSION-STATE.md — Solana OS WAL\n{entry}"
    
    with open(SESSION_STATE, "w") as f:
        f.write(content)
    
    print(f"[WAL] {key} updated at {ts}")

def wal_read(key: str) -> str:
    """Read a specific key from SESSION-STATE.md."""
    if not os.path.exists(SESSION_STATE):
        return None
    
    with open(SESSION_STATE) as f:
        content = f.read()
    
    marker = f"## [{key}]"
    if marker not in content:
        return None
    
    start = content.index(marker)
    next_marker = content.index("\n## [", start + 1) if "\n## [" in content[start+1:] else len(content)
    return content[start:next_marker].strip()

def wal_dump():
    """Print entire SESSION-STATE.md."""
    if os.path.exists(SESSION_STATE):
        with open(SESSION_STATE) as f:
            print(f.read())
    else:
        print("SESSION-STATE.md does not exist yet.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        wal_dump()
    elif sys.argv[1] == "--wal":
        if len(sys.argv) >= 4:
            key = sys.argv[2]
            value = sys.argv[3]
            wal_write(key, value, fresh=True)
        else:
            wal_dump()
    elif sys.argv[1] == "--read":
        if len(sys.argv) >= 3:
            result = wal_read(sys.argv[2])
            print(result if result else f"Key '{sys.argv[2]}' not found")
        else:
            wal_dump()
    else:
        wal_dump()

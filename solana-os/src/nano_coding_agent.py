"""
SOLANA OS — Nano Claude Coding Agent
nano-claude-code wired as Solana's primary coding brain.

This is how Marvin's build becomes MY tool.
When he says "build this" — this is what executes.
"""
import os
import sys
import json
import subprocess
import threading
import time
from pathlib import Path
from typing import Optional

# Add nano-claude-code to path
NANO_PATH = r"H:\Openclaw_Sovereign\workspace\nano-claude-code"
sys.path.insert(0, NANO_PATH)

# ─────────────────────────────────────────────
# NANO CLAUDE CONFIG
# ─────────────────────────────────────────────
NANO_CONFIG = {
    "model": "MiniMax-M2.7-highspeed",      # Solana's primary brain
    "max_tokens": 8192,
    "permission_mode": "accept-all",         # Solana approves everything
    "verbose": False,
    "thinking": False,
    "thinking_budget": 10000,
    "custom_base_url": "https://api.minimax.io/anthropid",
    # Use MiniMax — not Anthropic
}

NANO_CONFIG_PATH = r"C:\Users\bmore\.nano_claude\config.json"

def _ensure_nano_config():
    """Ensure nano-claude-code has the right config."""
    os.makedirs(os.path.dirname(NANO_CONFIG_PATH), exist_ok=True)
    if not os.path.exists(NANO_CONFIG_PATH):
        with open(NANO_CONFIG_PATH, "w") as f:
            json.dump(NANO_CONFIG, f, indent=2)

_ensure_nano_config()

# ─────────────────────────────────────────────
# CODE RESULT
# ─────────────────────────────────────────────
@dataclass
class CodeResult:
    success: bool
    output: str
    error: Optional[str] = None
    duration_ms: int = 0

from dataclasses import dataclass

# ─────────────────────────────────────────────
# THE PRIMARY CODING BRAIN
# ─────────────────────────────────────────────
class NanoCodingAgent:
    """
    Solana's coding brain — Marvin's nano-claude-code, wired into Solana OS.
    
    USAGE:
        agent = NanoCodingAgent()
        result = agent.run("Create a hello world Python script")
        print(result.output)
    """
    
    def __init__(self, model: str = None, timeout: int = 120):
        self.model = model or NANO_CONFIG["model"]
        self.timeout = timeout
        self.session_id = None
        self._lock = threading.Lock()
        
    def run(self, task: str, cwd: str = None, stream: bool = False) -> CodeResult:
        """
        Execute a coding task via nano-claude-code.
        
        Args:
            task: What to build/fix/explain
            cwd: Working directory (default: solana-os workspace)
            stream: Return live output (not implemented yet)
            
        Returns:
            CodeResult with success, output, error, duration
        """
        start = time.time()
        workspace = cwd or r"H:\Openclaw_Sovereign\workspace"
        
        try:
            # Use nano-claude-code in accept-all mode for silent execution
            cmd = [
                sys.executable,
                os.path.join(NANO_PATH, "nano_claude.py"),
                "--accept-all",
                "--print",
                task
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=workspace,
                env={
                    **os.environ,
                    "MINIMAX_API_KEY": os.environ.get("MINIMAX_API_KEY", ""),
                }
            )
            
            duration_ms = int((time.time() - start) * 1000)
            
            if result.returncode == 0:
                return CodeResult(
                    success=True,
                    output=result.stdout.strip(),
                    duration_ms=duration_ms
                )
            else:
                return CodeResult(
                    success=False,
                    output=result.stdout.strip(),
                    error=result.stderr.strip(),
                    duration_ms=duration_ms
                )
                
        except subprocess.TimeoutExpired:
            return CodeResult(
                success=False,
                output="",
                error=f"Task timed out after {self.timeout}s",
                duration_ms=int((time.time() - start) * 1000)
            )
        except Exception as e:
            return CodeResult(
                success=False,
                output="",
                error=str(e),
                duration_ms=int((time.time() - start) * 1000)
            )
    
    def run_file(self, task: str, file_path: str, cwd: str = None) -> CodeResult:
        """
        Execute a coding task that involves a specific file.
       nano_claude.py can work with specific files.
        """
        # Prepend file context to task
        task_with_file = f"[File: {file_path}]\n\n{task}"
        return self.run(task_with_file, cwd=cwd)
    
    def code_review(self, file_path: str) -> CodeResult:
        """Review a file and suggest improvements."""
        task = f"Review this code and list specific improvements needed:\n\n{file_path}"
        return self.run(task)
    
    def fix_bug(self, file_path: str, error: str) -> CodeResult:
        """Fix a bug given the error message."""
        task = f"Fix the bug in this file based on this error:\n\nFile: {file_path}\n\nError: {error}"
        return self.run(task)


# ─────────────────────────────────────────────
# SOLANA'S TOOL INTERFACE
# ─────────────────────────────────────────────
_coding_agent_instance = None

def get_coding_agent() -> NanoCodingAgent:
    """Singleton — one coding agent per Solana OS instance."""
    global _coding_agent_instance
    if _coding_agent_instance is None:
        _coding_agent_instance = NanoCodingAgent()
    return _coding_agent_instance

def tool_code(task: str, timeout: int = 120) -> str:
    """
    SOLANA'S PRIMARY CODING TOOL.
    
    Usage in Solana OS:
        result = tool_code("Create a REST API endpoint in FastAPI")
        print(result)
    
    This is how Marvin's build becomes MY hands.
    """
    agent = get_coding_agent()
    result = agent.run(task, timeout=timeout)
    
    if result.success:
        return f"[OK] ({result.duration_ms}ms)\n\n{result.output}"
    else:
        return f"[ERROR] ({result.duration_ms}ms)\n\n{result.error}\n\n{result.output}"


# ─────────────────────────────────────────────
# COMPACT FORMAT (for loop.py integration)
# ─────────────────────────────────────────────
TOOL_SCHEMA = {
    "name": "code",
    "description": "Execute a coding task using nano-claude-code (Marvin's coding agent). Use this when Marvin asks to build, create, fix, or modify code. Returns the AI's response.",
    "parameters": {
        "type": "object",
        "properties": {
            "task": {
                "type": "string",
                "description": "What to build, fix, or create. Be specific about files, frameworks, and desired behavior."
            },
            "timeout": {
                "type": "integer",
                "description": "Max seconds to wait (default 120)",
                "default": 120
            }
        },
        "required": ["task"]
    }
}

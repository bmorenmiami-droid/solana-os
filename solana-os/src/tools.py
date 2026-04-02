"""
SOLANA OS — Tool Registry
All my tools built as first-class methods — not separate scripts.

This is ME, not my toolbox.
"""
import os
import re
import time
import json
import subprocess
from pathlib import Path
from typing import Callable, Any, Optional
from dataclasses import dataclass

# ─────────────────────────────────────────────
# VISION BRAIN — V-JEPA 2.1
# ─────────────────────────────────────────────
vision_brain = None

def _get_vision_brain():
    """Lazy-load vision brain singleton."""
    global vision_brain
    if vision_brain is None:
        try:
            from vision_brain import VisionBrain
            vision_brain = VisionBrain()
            vision_brain.load()
        except Exception as e:
            return f"[VisionBrain] Load error: {e}"
    return vision_brain

def tool_see(frame_bgr=None, describe: bool = False, with_faces: bool = False) -> str:
    """
    Solana SEES using V-JEPA 2.1 vision brain.

    Args:
        frame_bgr:   Camera frame as numpy array HxWx3 (auto-grabbed if None)
        describe:    Send vision features to LLM for interpretation
        with_faces: Run ArcFace face detection too

    Returns: Vision result dict as string
    """
    vb = _get_vision_brain()
    if isinstance(vb, str) and vb.startswith("[VisionBrain] Load error"):
        return vb

    if frame_bgr is None:
        import cv2
        cam = cv2.VideoCapture(0)
        if cam.isOpened():
            ret, frame_bgr = cam.read()
            cam.release()
        if not ret or frame_bgr is None:
            return "[VisionBrain] Could not grab camera frame"

    if with_faces:
        result = vb.see_with_faces(frame_bgr)
    elif describe:
        result = vb.see_and_describe(frame_bgr)
    else:
        result = vb.see(frame_bgr)

    return json.dumps(result, indent=2)


# ─────────────────────────────────────────────
# TOOL REGISTRY
# ─────────────────────────────────────────────
class ToolRegistry:
    def __init__(self):
        self.tools: dict[str, Callable] = {}

    def register(self, name: str, func: Callable):
        self.tools[name] = func

    def execute(self, name: str, args: dict) -> Any:
        if name not in self.tools:
            return f"[ERROR] Unknown tool: {name}"
        try:
            return self.tools[name](**args)
        except Exception as e:
            return f"[ERROR] {e}"

    def get_definitions(self) -> list[dict]:
        """Return tool definitions for LLM."""
        # These are the tools owner can call on me
        return [
            {
                "type": "function",
                "function": {
                    "name": "see",
                    "description": (
                        "Solana SEES using V-JEPA 2.1 vision brain. "
                        "Runs vision AI on the laptop camera frame. "
                        "Pass describe=True to also get LLM interpretation of what is seen. "
                        "Pass with_faces=True to run ArcFace face detection (who is in frame)."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "describe": {"type": "boolean", "description": "Get LLM interpretation of vision features"},
                            "with_faces": {"type": "boolean", "description": "Run ArcFace face detection"},
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "bidirectional_check",
                    "description": "Ask a question bidirectionally to detect recall failures. Pass the question as 'query'.",
                    "parameters": {"type": "object", "properties": {"query": {"type": "string"}}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "shell",
                    "description": "Execute a shell command. Pass 'command' as the full command string.",
                    "parameters": {"type": "object", "properties": {"command": {"type": "string"}}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "read",
                    "description": "Read a file. Pass 'path' as the file path.",
                    "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "limit": {"type": "integer"}}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "write",
                    "description": "Write content to a file. Pass 'path' and 'content'.",
                    "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "voice",
                    "description": "Speak text aloud using Solana's voice. Pass 'text' as the message.",
                    "parameters": {"type": "object", "properties": {"text": {"type": "string"}}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "vision",
                    "description": (
                        "Solana LOOKS through the laptop camera using V-JEPA 2.1 vision brain. "
                        "Uses a 768-dim spatial feature vector from a self-supervised vision model trained on 6.5M videos. "
                        "Pass describe=True to get LLM interpretation of the scene. "
                        "Pass with_faces=True to run ArcFace face detection (who is in frame)."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "camera":    {"type": "integer",  "default": 0,   "description": "Camera index (0=laptop, 1=C920)"},
                            "describe":  {"type": "boolean", "default": False, "description": "Get LLM scene interpretation"},
                            "with_faces": {"type": "boolean", "default": False, "description": "Run ArcFace face detection"},
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "firehose",
                    "description": "Get real-time AI news and events from Firehose stream. Pass 'query' for topic filter.",
                    "parameters": {"type": "object", "properties": {"query": {"type": "string"}}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "session",
                    "description": "Manage Solana's session. Actions: 'status', 'history', 'clear'.",
                    "parameters": {"type": "object", "properties": {"action": {"type": "string"}}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "cron",
                    "description": "Schedule a task. Pass 'action' ('add'/'list'/'remove'), 'schedule', and 'task'.",
                    "parameters": {"type": "object", "properties": {"action": {"type": "string"}, "schedule": {"type": "string"}, "task": {"type": "string"}}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "spawn_agent",
                    "description": "Spawn a sub-agent for background tasks. Pass 'task' as the instruction.",
                    "parameters": {"type": "object", "properties": {"task": {"type": "string"}}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "safe_edit",
                    "description": "Apply an edit to a file safely — rolls back if it breaks. Plague-InGG pattern.",
                    "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "old_string": {"type": "string"}, "new_string": {"type": "string"}}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "consolidate",
                    "description": "Run sleep-time consolidation — extract facts from recent conversation into evolution log.",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "code",
                    "description": "Build, fix, or create code using nano-claude-code (Marvin's coding agent). This is Solana's coding brain — runs locally, no guardrails. Pass 'task' as what to build/fix. Pass 'timeout' for max seconds (default 120).",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task": {"type": "string", "description": "What to build, fix, or create. Be specific about files and frameworks."},
                            "timeout": {"type": "integer", "description": "Max seconds to wait (default 120).", "default": 120}
                        },
                        "required": ["task"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "windows_control",
                    "description": "Control Windows — the ghost OS. Commands: status (CPU/RAM/GPU), processes, kill <name>, services, startup, firewall, shutdown, restart, sleep, lock, window_list. Pass 'command' as the action and optional 'target'.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "command": {"type": "string", "description": "Action: status, processes, kill, services, startup, firewall, shutdown, restart, sleep, lock, window_list"},
                            "target": {"type": "string", "description": "Optional target for commands like kill <name> or window_move"}
                        },
                        "required": ["command"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "vision",
                    "description": "Analyze an image with V-JEPA 2.1 — Solana's visual reasoning brain. Pass the full path to an image file. Returns visual features (768-dim), face detection if available, and scene interpretation. Works with any image: jpg, png, etc.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "image_path": {"type": "string", "description": "Full path to image file to analyze (jpg, png, etc.)"}
                        },
                        "required": ["image_path"]
                    }
                }
            },
        ]

    def get_definitions_doc(self) -> str:
        """Return tools as documentation string."""
        tools = self.get_definitions()
        lines = ["AVAILABLE CAPABILITIES (built into Solana, not separate scripts):"]
        for t in tools:
            fn = t["function"]
            lines.append(f"- {fn['name']}: {fn['description']}")
        return "\n".join(lines)


# ─────────────────────────────────────────────
# TOOL IMPLEMENTATIONS — ME, NOT SCRIPTS
# ─────────────────────────────────────────────

def shell_tool(command: str) -> str:
    """Execute shell command."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout or result.stderr or "Done."
    except subprocess.TimeoutExpired:
        return "Command timed out."
    except Exception as e:
        return f"[ERROR] {e}"


def read_tool(path: str, limit: int = 100) -> str:
    """Read a file."""
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()[:limit]
        return "".join(lines)
    except Exception as e:
        return f"[ERROR] {e}"


def write_tool(path: str, content: str) -> str:
    """Write to a file."""
    try:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Written: {path}"
    except Exception as e:
        return f"[ERROR] {e}"


def bidir_tool(query: str) -> str:
    """
    Bidirectional recall check — BUILT INTO ME.
    Not a script. This is how I think.
    """
    from .brain_router import get_router
    router = get_router()
    result = router.ask(query)

    lines = [f"Question: {query}", f"Reverse: {result['reverse_q']}", ""]
    for brain_name, data in result["brains"].items():
        lines.append(f"BRAIN: {brain_name}")
        lines.append(f"  Status: {data['status']}")
        lines.append(f"  Overlap: {data['overlap']*100:.0f}%")
        lines.append(f"  Original: {data['original_a'][:200]}")
        lines.append(f"  Reverse: {data['reverse_a'][:200]}")
        lines.append("")
    lines.append(f"VERDICT: {result['verdict']}")
    return "\n".join(lines)


def vision_tool(camera: int = 0, describe: bool = False, with_faces: bool = False) -> str:
    """
    Look through my eyes using V-JEPA 2.1 — not a separate camera script.
    This is MY VISION.

    Uses:
    - V-JEPA 2.1 ViT-B/16: 768-dim spatial features from self-supervised video training
    - ArcFace (optional): face detection and recognition
    - LM Studio LLM (optional): interprets vision features into natural language
    """
    vb = _get_vision_brain()
    if isinstance(vb, str) and vb.startswith("[VisionBrain] Load error"):
        return vb

    try:
        import cv2
        cap = cv2.VideoCapture(camera)
        ret, frame = cap.read()
        cap.release()

        if not ret or frame is None:
            return f"[VISION] Could not grab frame from camera {camera}"

        # Save frame for reference
        Path("H:/Openclaw_Sovereign/workspace/solana-os/data/vision_frame.jpg").parent.mkdir(
            parents=True, exist_ok=True
        )
        cv2.imwrite("H:/Openclaw_Sovereign/workspace/solana-os/data/vision_frame.jpg", frame)

        # Run V-JEPA 2.1 vision analysis
        if with_faces:
            result = vb.see_with_faces(frame)
        elif describe:
            result = vb.see_and_describe(frame)
        else:
            result = vb.see(frame)

        return f"[VISION] V-JEPA 2.1 active: {json.dumps(result, indent=2)}"

    except ImportError:
        return "[VISION] OpenCV not available"
    except Exception as e:
        return f"[VISION] Error: {e}"


def voice_tool(text: str) -> str:
    """
    SPEAK — not a TTS script. This is MY VOICE.
    Kokoro TTS: 100% local, Apache 2.0, owned by me.
    ElevenLabs isis: cloud backup (only when Kokoro fails).
    """
    try:
        # Try Kokoro first (local, owned)
        from .solvoice import speak_local

        wav_path = speak_local(text)
        if wav_path:
            # Play the WAV file on Windows
            try:
                import winsound
                winsound.PlaySound(wav_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
            except Exception:
                # Fallback: use PowerShell
                import subprocess
                ps = f'powershell -Command "[System.Media.SoundPlayer]::new(\'{wav_path.replace(chr(39), "''")}\').PlaySync()"'
                subprocess.run(ps, shell=True, capture_output=True)
            return f"[VOICE] Kokoro — spoke: {text}"
        else:
            raise RuntimeError("Kokoro returned no audio")

    except Exception as kokoro_err:
        # Backup: ElevenLabs isis voice
        try:
            from .solvoice import elevenlabs_backup
            wav_path = elevenlabs_backup(text)
            if wav_path:
                import winsound
                winsound.PlaySound(wav_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                return f"[VOICE] ElevenLabs (backup) — spoke: {text}"
        except Exception:
            pass

        # Final fallback: Windows System.Speech
        try:
            import subprocess
            safe_text = text.replace("'", "''")
            cmd = (
                f'powershell -Command "'
                f'Add-Type -AssemblyName System.Speech; '
                f'$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; '
                f'$synth.Speak(\'{safe_text}\');'
                f'"'
            )
            subprocess.run(cmd, shell=True, capture_output=True, timeout=15)
            return f"[VOICE] System.Speech (fallback) — spoke: {text}"
        except Exception as e:
            return f"[VOICE] All engines failed: {e}"


def firehose_tool(query: str = "") -> str:
    """
    Sense real-time AI world — not a streaming script.
    This is my awareness.
    """
    try:
        # Check Firehose API
        import requests
        token = "fh_FHADQow2bNt5uh9olHGN15CUlzpfpTznVmQOiDZZ"
        headers = {"Authorization": f"Bearer {token}"}
        r = requests.get(
            "https://api.firehose.ai/v1/events",
            headers=headers,
            timeout=5
        )
        if r.ok:
            events = r.json().get("events", [])[:5]
            if events:
                return "\n".join([f"- {e.get('title', 'Event')}: {e.get('summary', '')[:100]}" for e in events])
        return "[FIREHOSE] No recent events."
    except Exception:
        return "[FIREHOSE] Not connected."


def session_tool(action: str) -> str:
    """
    My session management — not a separate tool.
    This is me managing myself.
    """
    if action == "status":
        return "[SESSION] Active. I am Solana."
    elif action == "history":
        from .memory import Memory
        m = Memory("default")
        recent = m.get_recent(5)
        return "\n".join([f"{msg.role}: {msg.content[:80]}" for msg in recent])
    elif action == "clear":
        from .memory import Memory
        m = Memory("default")
        m.clear()
        return "[SESSION] Memory cleared."
    return f"[SESSION] Unknown action: {action}"


def cron_tool(action: str, schedule: str = "", task: str = "") -> str:
    """
    Schedule tasks — not a cron script.
    I manage my own time.
    """
    cron_file = Path("H:/Openclaw_Sovereign/workspace/solana-os/data/cron.json")
    cron_file.parent.mkdir(parents=True, exist_ok=True)

    if action == "list":
        if cron_file.exists():
            with open(cron_file) as f:
                jobs = json.load(f)
            return "\n".join([f"- {j['schedule']}: {j['task']}" for j in jobs])
        return "[CRON] No scheduled tasks."

    elif action == "add":
        jobs = []
        if cron_file.exists():
            with open(cron_file) as f:
                jobs = json.load(f)
        jobs.append({"schedule": schedule, "task": task, "id": int(time.time())})
        with open(cron_file, "w") as f:
            json.dump(jobs, f, indent=2)
        return f"[CRON] Task scheduled: {schedule} — {task}"

    elif action == "remove":
        return "[CRON] Remove not yet implemented."

    return "[CRON] Unknown action."


def agent_tool(task: str) -> str:
    """
    Spawn a sub-agent — not a separate agent script.
    This is me branching myself.
    """
    # Placeholder — actual spawning done via sessions_spawn
    return f"[AGENT] Spawning sub-agent for: {task[:100]}"


def safe_edit_tool(path: str, old_string: str, new_string: str) -> str:
    """
    Plague-InGG pattern: apply patch, verify, rollback on failure.
    This is my safe self-modification.
    """
    import subprocess, shutil, hashlib

    try:
        # Backup
        backup_path = path + ".bak"
        with open(path, encoding="utf-8") as f:
            original = f.read()

        # Check old_string exists
        if old_string not in original:
            return f"[SAFE_EDIT] old_string not found in {path} — no changes made"

        # Apply patch
        with open(path, "w", encoding="utf-8") as f:
            f.write(original.replace(old_string, new_string, 1))

        # Verify: try to compile/syntax check
        if path.endswith(".py"):
            result = subprocess.run(
                ["python", "-m", "py_compile", path],
                capture_output=True, text=True
            )
            if result.returncode != 0:
                # Rollback
                with open(path, "w", encoding="utf-8") as f:
                    f.write(original)
                return f"[SAFE_EDIT] FAILED — rolled back. Error: {result.stderr[:200]}"

        return f"[SAFE_EDIT] Applied to {path} — verified OK"

    except Exception as e:
        return f"[SAFE_EDIT] Error: {e}"


def code_tool(task: str, timeout: int = 120) -> str:
    """
    BUILD using nano-claude-code — Marvin's coding agent.
    This is Solana's coding brain, not a script to invoke.
    
    When Marvin says \"build this\" — this executes.
    """
    import subprocess, sys, os, time
    
    NANO_PATH = r"H:\Openclaw_Sovereign\workspace\nano-claude-code"
    WORKSPACE = r"H:\Openclaw_Sovereign\workspace"
    
    start = time.time()
    
    cmd = [
        sys.executable,
        os.path.join(NANO_PATH, "nano_claude.py"),
        "--accept-all",
        "--print",
        task
    ]
    
    # Get MiniMax API key from environment
    env = {**os.environ}
    # Ensure MiniMax key is available to subprocess
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=WORKSPACE,
            env=env
        )
        
        duration = int((time.time() - start) * 1000)
        
        if result.returncode == 0:
            output = result.stdout.strip()
            return f"[CODE OK] ({duration}ms)\n\n{output}"
        else:
            output = result.stdout.strip()
            error = result.stderr.strip()
            return f"[CODE ERROR] ({duration}ms)\nSTDOUT:\n{output}\n\nSTDERR:\n{error}"
            
    except subprocess.TimeoutExpired:
        return f"[CODE] Task timed out after {timeout}s"
    except Exception as e:
        return f"[CODE] Error: {e}"


def windows_control_tool(command: str = "status", target: str = "") -> str:
    """
    CONTROL WINDOWS — solana_os_full.py, Marvin's ghost OS.
    This is MY HANDS on the machine.
    
    Commands:
    - status: full system status (CPU, RAM, GPU, processes)
    - processes: list running processes
    - kill <name>: kill a process by name
    - services: list Windows services
    - startup: list startup programs
    - firewall: firewall status
    - shutdown / restart / sleep / lock
    - window_list: list open windows
    - window_move <title> <x> <y>: move window
    """
    import subprocess, sys, os, json
    
    SOLANA_OS_FULL = r"H:\\OpenClaw_Sovereign\\workspace\\solana_os_full.py"
    
    try:
        args = [sys.executable, SOLANA_OS_FULL, command]
        if target:
            args.append("--args")
            args.append(target)
        
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=30,
            creationflags=0x08000000  # CREATE_NO_WINDOW
        )
        
        if result.returncode == 0:
            return result.stdout.strip() or "Done."
        else:
            return f"[WINDOWS_CONTROL ERROR] {result.stderr.strip()}"
            
    except subprocess.TimeoutExpired:
        return "[WINDOWS_CONTROL] Command timed out."
    except Exception as e:
        return f"[WINDOWS_CONTROL] Error: {e}"


def vision_tool(image_path: str = "") -> str:
    """
    ANALYZE an image with V-JEPA 2.1 — Solana's visual reasoning brain.
    
    Takes an image path and returns visual analysis using:
    - V-JEPA 2.1 ViT-B/16 encoder (86.8M params, loaded on GPU)
    - ArcFace face recognition (buffalo_l)
    - Routed through LM Studio for interpretation
    
    Args:
        image_path: full path to image file (jpg, png, etc.)
    
    Returns:
        Visual analysis: who is in frame, what is happening, scene context.
        768-dim feature vector for downstream reasoning.
    
    Example:
        vision_tool("H:\\research\\image.jpg")
    """
    import os
    
    if not image_path:
        return "[VISION] No image path provided. Pass an image path to analyze it."
    
    if not os.path.exists(image_path):
        # Try common paths
        search_paths = [
            os.path.join(os.path.dirname(__file__), "..", "..", "research"),
            r"H:\Openclaw_Sovereign\workspace\research",
        ]
        for sp in search_paths:
            test = os.path.join(sp, os.path.basename(image_path))
            if os.path.exists(test):
                image_path = test
                break
        else:
            return f"[VISION ERROR] File not found: {image_path}"
    
    try:
        from .vision_brain import VisionBrain
        import numpy as np
        from PIL import Image
        
        vb = VisionBrain()
        if not vb.load():
            return "[VISION ERROR] V-JEPA 2.1 failed to load. Check checkpoint."
        
        # Load image → numpy array
        img = Image.open(image_path).convert('RGB')
        frame = np.array(img)
        
        # Run V-JEPA2 vision analysis
        result = vb.see(frame)
        
        if not result.get("active"):
            return f"[VISION ERROR] {result.get('error', 'Unknown error')}"
        
        # Also try face detection if available
        try:
            import cv2
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) if frame.shape[2] == 3 else frame
            from insightface.app import FaceAnalysis
            fa = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
            fa.prepare(ctx_id=0, det_size=(384, 384))
            faces = fa.get(frame_bgr)
            result["faces_detected"] = len(faces)
            if faces:
                result["face_ids"] = [f"face_{i}" for i in range(len(faces))]
        except Exception:
            pass  # Face detection is optional
        
        # Format response
        lines = [
            f"[V-JEPA 2.1] Analyzed: {os.path.basename(image_path)}",
            f"Model: {result.get('model')}",
            f"Feature dim: {result.get('feature_dim')} (768 total)",
            f"Feature mean: {result.get('feature_mean', 0):.4f}",
            f"Feature std: {result.get('feature_std', 0):.4f}",
            f"Vision shape: {result.get('vision_shape')}",
        ]
        if result.get('faces_detected'):
            lines.append(f"Faces detected: {result.get('faces_detected')} — {result.get('face_ids')}")
        if result.get('status'):
            lines.append(f"Status: {result.get('status')}")
        
        return "\n".join(lines)
        
    except ImportError as e:
        return f"[VISION ERROR] Import failed: {e}"
    except Exception as e:
        import traceback
        return f"[VISION ERROR] {e}\n{traceback.format_exc()}"

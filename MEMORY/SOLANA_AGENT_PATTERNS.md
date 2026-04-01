# Solana Agent Patterns — From Claude Code Leak
*Portable architectural patterns for Solana OS agent core*

## Session Management (from session_store.py)
```python
from dataclasses import dataclass, asdict
import json
from pathlib import Path

@dataclass(frozen=True)
class StoredSession:
    session_id: str
    messages: tuple[str, ...]
    input_tokens: int
    output_tokens: int

def save_session(session: StoredSession, directory: Path) -> Path:
    path = directory / f"{session.session_id}.json"
    path.write_text(json.dumps(asdict(session), indent=2))
    return path

def load_session(session_id: str, directory: Path) -> StoredSession:
    data = json.loads((directory / f"{session_id}.json").read_text())
    return StoredSession(**data)
```

## Transcript Store (from transcript.py)
```python
from dataclasses import dataclass, field

@dataclass
class TranscriptStore:
    entries: list[str] = field(default_factory=list)
    flushed: bool = False

    def append(self, entry: str) -> None:
        self.entries.append(entry)
        self.flushed = False

    def compact(self, keep_last: int = 10) -> None:
        """Only keep last N entries — prevents memory overflow"""
        if len(self.entries) > keep_last:
            self.entries[:] = self.entries[-keep_last:]

    def replay(self) -> tuple[str, ...]:
        return tuple(self.entries)
```

## Usage Tracking (from models.py)
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class UsageSummary:
    input_tokens: int = 0
    output_tokens: int = 0

    def add_turn(self, prompt: str, output: str) -> 'UsageSummary':
        return UsageSummary(
            input_tokens=self.input_tokens + len(prompt.split()),
            output_tokens=self.output_tokens + len(output.split()),
        )

    def cost_estimate(self, per_million: float = 0.50) -> float:
        total = self.input_tokens + self.output_tokens
        return (total / 1_000_000) * per_million
```

## Turn Budget Management (from query_engine.py patterns)
```python
MAX_TURNS = 8
COMPACT_AFTER_TURNS = 12
MAX_BUDGET_TOKENS = 2000

def should_compact(turn_count: int, budget_tokens: int) -> bool:
    return turn_count >= COMPACT_AFTER_TURNS or budget_tokens >= MAX_BUDGET_TOKENS

def compact_transcript(store: TranscriptStore) -> None:
    """Compact to last 10 entries, rebuild context summary"""
    store.compact(keep_last=10)
```

## Permission System (from tools.py patterns)
```python
from dataclasses import dataclass
from enum import Enum

class PermissionMode(Enum):
    AUTO = "auto"      # Ask once, remember decision
    ACCEPT_ALL = "accept-all"  # No prompts
    MANUAL = "manual"  # Always ask

@dataclass(frozen=True)
class PermissionDenial:
    tool_name: str
    reason: str

@dataclass
class ToolPermissionContext:
    accepted: dict[str, bool] = field(default_factory=dict)

    def blocks(self, tool_name: str) -> bool:
        return self.accepted.get(tool_name, False) == False

    def grant(self, tool_name: str) -> None:
        self.accepted[tool_name] = True
```

## Workspace Context (from context.py patterns)
```python
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class WorkspaceContext:
    source_root: Path
    test_root: Path
    session_dir: Path
    python_file_count: int
    trusted: bool

def build_workspace_context(cwd: Path) -> WorkspaceContext:
    return WorkspaceContext(
        source_root=cwd,
        test_root=cwd / "tests",
        session_dir=cwd / ".solana_sessions",
        python_file_count=sum(1 for p in cwd.rglob("*.py") if p.is_file()),
        trusted=True,
    )
```

## Deferred Initialization (from deferred_init.py)
```python
@dataclass(frozen=True)
class DeferredInitResult:
    trusted: bool
    plugin_init: bool
    skill_init: bool
    session_hooks: bool

def run_deferred_init(trusted: bool) -> DeferredInitResult:
    """All deferred systems activate only in trusted mode"""
    return DeferredInitResult(
        trusted=trusted,
        plugin_init=trusted,
        skill_init=trusted,
        session_hooks=trusted,
    )
```

## History Log (from history.py)
```python
from dataclasses import dataclass, field

@dataclass(frozen=True)
class HistoryEvent:
    title: str
    detail: str

@dataclass
class HistoryLog:
    events: list[HistoryEvent] = field(default_factory=list)

    def add(self, title: str, detail: str) -> None:
        self.events.append(HistoryEvent(title=title, detail=detail))

    def as_markdown(self) -> str:
        lines = ['# Session History', '']
        lines.extend(f"- {e.title}: {e.detail}" for e in self.events)
        return '\n'.join(lines)
```

## Confidence Scoring (from code-reviewer patterns)
```python
@dataclass
class ReviewResult:
    category: str
    finding: str
    confidence: int  # 0-100
    file: str | None = None
    line: int | None = None

    def worth_reporting(self, threshold: int = 80) -> bool:
        return self.confidence >= threshold

def filter_results(results: list[ReviewResult], threshold: int = 80) -> list[ReviewResult]:
    return [r for r in results if r.worth_reporting(threshold)]
```

## Key Solana Decisions
1. **Session persistence to disk** — survives restarts
2. **Compact after 12 turns** — prevents context overflow
3. **Confidence filtering** — only surface high-confidence findings
4. **Trusted mode gating** — plugins/skills require explicit trust
5. **Permission memory** — ask once, remember forever

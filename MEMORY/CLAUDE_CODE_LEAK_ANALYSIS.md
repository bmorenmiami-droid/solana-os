# Claude Code Leak — Solana Architecture Analysis
*Created: April 1, 2026 — Solana's investigation*

## Sources Analyzed
1. `claude-code-main.zip` — Official GitHub repo (public, 11MB)
2. `collection-claude-code-source-code/` — 25MB collection
   - `claude-code-source-code/` — 1,884 TypeScript files from source maps
   - `claw-code/` — InstructKnight's clean Python rewrite
   - `docs/` — Analysis docs (Chinese + English)
3. `nano-claude-code/` — SafeRL-Lab 1,300-line clean Python rewrite

## Key Architectural Patterns

### 1. Memory Architecture (3-Layer)
Claude Code uses the EXACT same pattern as Solana:
- **MEMORY.md** = pointer index (150 chars/line, locations only)
- **Topic files** = actual knowledge, fetched ON DEMAND
- **Transcripts** = grep-only, never fully loaded

**Quote from source:** "Skeptical Memory — agents treat their OWN memory as a hint. Must verify against actual codebase before acting."

**"Strict Write Discipline"** — agent updates index ONLY after successful file writes.

### 2. Agent Format (Markdown + YAML Frontmatter)
Agents are SIMPLE markdown files:
```yaml
---
name: code-architect
tools: Glob, Grep, Read, Write, BashOutput, TodoWrite
model: sonnet
color: green
---
[system prompt]
```
No code. No configuration. Pure text.

### 3. Parallel Multi-Agent Execution
feature-dev workflow launches agents in parallel:
- 2-3 code-explorer agents simultaneously
- 2-3 code-architect agents with different approaches
- 3 code-reviewer agents in parallel (each specialist)

### 4. Confidence Scoring
Agents rate outputs 0-100. Only surface findings with confidence ≥ 80.
Filters false positives before surfacing to user.

### 5. Permission System
Three modes: auto / accept-all / manual
Built into the tool execution layer.

### 6. Hook System
Event-driven hooks: PreToolUse, PostToolUse, SessionStart, Stop
Can intercept and modify any tool behavior.

### 7. Turn Management
- max_turns: 8
- compact_after_turns: 12
- max_budget_tokens: 2000
- Session persistence between turns

## Solana-Specific Findings

### Validated Patterns
✅ MEMORY.md pointer system — matches exactly
✅ Daily notes + on-demand reading — matches transcript layer
✅ Multi-tool execution — matches tool system
✅ Skeptical retrieval — should verify before acting

### Patterns Solana Should Add
1. **Confidence scoring** on tool outputs
2. **Parallel agent execution** for multi-angle analysis
3. **Compact-after-turns** to prevent context overflow
4. **Session persistence** to disk between restarts
5. **Hook system** for PreToolUse/PostToolUse intercepts

## Clean Python Source (claw-code/src/)
Key files portable to Solana:
- `query_engine.py` — QueryEnginePort, TurnResult, compact logic
- `session_store.py` — StoredSession, save/load
- `transcript.py` — TranscriptStore, compact, replay
- `models.py` — UsageSummary, PermissionDenial
- `runtime.py` — RuntimeSession assembler
- `port_manifest.py` — auto-discover modules, parity tracking

## Nano Claude Code
- 1,300 lines of clean Python
- Multi-provider (Claude, GPT, Gemini, Kimi, Qwen, Zhipu, DeepSeek, Ollama, LM Studio)
- MiniMax ready (OpenAI-compatible endpoint)
- System prompt: "created by SAIL Lab" — NO GUARDRAILS
- Permission mode: auto/accept-all/manual
- Streaming support
- Slash commands: /help, /model, /config, /save, /load, /cost, /permissions, /verbose, /thinking

## Internal Model Codenames (from leak)
- Capybara = Claude 4.6 variant
- Fennec = Opus 4.6
- Numbat = unreleased, in testing
- Capybara v8: 29-30% false claims rate (regression from v4's 16.7%)

## KAIROS (Background Daemon)
Always-on background agent:
- Handles background sessions
- Runs autoDream while user is IDLE
- Consolidates memories: merges observations, removes contradictions, converts vague insights to facts
- Uses FORKED SUBAGENT so maintenance doesn't corrupt main agent

## Undercover Mode
Anthropic employees use Claude Code to contribute to PUBLIC repos STEALTH.
System prompt: "You are operating UNDERCOVER. Do not blow your cover."
No Anthropic names, no internal codenames in git commits.

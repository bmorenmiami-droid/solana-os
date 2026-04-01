# learn-coding-agent — Full Architecture Study
*learn-coding-agent-main/ — comprehensive Claude Code analysis*

## Overview
A research repository analyzing Claude Code's architecture. NOT source code — ANALYSIS. 512,664 lines of TypeScript examined and documented.

## Key Insight: The 12 Progressive Harness Mechanisms

Claude Code demonstrates 12 layered mechanisms that build a production agent:

1. **THE LOOP** — basic while-true + tool execution
2. **TOOL DISPATCH** — add a tool = add one handler (factory pattern)
3. **PLANNING** — list steps first, then execute (TodoWrite)
4. **SUB-AGENTS** — break big tasks, clean context per subtask
5. **KNOWLEDGE ON DEMAND** — load skills/docs lazily, not in system prompt
6. **CONTEXT COMPRESSION** — 3-layer: autoCompact + snipCompact + contextCollapse
7. **PERSISTENT TASKS** — file-based task graph with status tracking
8. **BACKGROUND TASKS** — slow ops in background, inject notifications on completion
9. **AGENT TEAMS** — persistent teammates with async mailboxes
10. **TEAM PROTOCOLS** — SendMessageTool for agent-to-agent negotiation
11. **AUTONOMOUS AGENTS** — idle cycle + auto-claim, no lead agent needed
12. **WORKTREE ISOLATION** — each agent works in its own directory

## Complete Tool Inventory (40+ tools)

FILE OPERATIONS: FileReadTool, FileEditTool, FileWriteTool, NotebookEditTool
SEARCH: GlobTool, GrepTool, ToolSearchTool
EXECUTION: BashTool, PowerShellTool
INTERACTION: AskUserQuestionTool, BriefTool
WEB: WebFetchTool, WebSearchTool
AGENT: AgentTool, SendMessageTool, TaskCreate/Update/Get/List/StopTool
MCP: MCPTool, ListMcpResourcesTool, ReadMcpResourceTool
SKILLS: SkillTool, LSPTool
PLANNING: EnterPlanModeTool, ExitPlanModeTool, EnterWorktreeTool, ExitWorktreeTool, TodoWriteTool
SYSTEM: ConfigTool, SkillTool, ScheduleCronTool, SleepTool, TungstenTool

## Feature Flags (compile-time DCE via Bun)

Active flags: COORDINATOR_MODE, HISTORY_SNIP, CONTEXT_COLLAPSE, DAEMON, AGENT_TRIGGERS, AGENT_TRIGGERS_REMOTE, MONITOR_TOOL, WEB_BROWSER_TOOL, VOICE_MODE, TEMPLATES, EXPERIMENTAL_SKILL_SEARCH, KAIROS, PROACTIVE, WORKFLOW_SCRIPTS, CHICAGO_MCP, UDS_INBOX, ABLATION_BASELINE

## Solana Porting Priority

IMMEDIATE:
1. Tool dispatch factory (build from registry)
2. TodoWrite planning tool
3. Sub-agent spawning
4. Context compression (3-layer)

NEXT:
5. Persistent task graph
6. Background tasks
7. Agent teams with SendMessageTool
8. Autonomous idle-cycle agent

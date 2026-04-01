# Solana Feature-Dev Skill
## Based on Anthropic Claude Code's feature-dev workflow (leaked 2026-03-31)

## Overview
Ported from: `claude-code-leak/claude-code-main/plugins/feature-dev/`

A 7-phase structured feature development workflow. Launch multiple specialized agents in parallel at each phase. User confirms between every phase.

---

## The 7 Phases

### Phase 1: Discovery
**Goal:** Clarify what needs to be built.

Ask:
- What problem does this solve?
- What should the feature do?
- Who is the user?
- What does success look like?

If feature is underspecified → ask questions first.

---

### Phase 2: Exploration
**Goal:** Understand the codebase deeply.

Launch 2-3 `code-explorer` agents IN PARALLEL:
- Agent 1: Trace execution paths through the relevant module
- Agent 2: Find patterns in similar features
- Agent 3: Map dependencies and data flows

Ask agents to return: "Here are the 10 most important files to read."
After agents complete → read those files to build context.

---

### Phase 3: Questions
**Goal:** Ask ALL clarifying questions before designing.

Ask user about:
- Edge cases
- Performance constraints
- Compatibility requirements
- Error handling philosophy
- Testing requirements

**Wait for user answers.** Do not proceed until all questions are answered.

---

### Phase 4: Architecture Design
**Goal:** Design the implementation approach.

Launch 2-3 `code-architect` agents IN PARALLEL, each with a different approach:
- Agent 1 (Minimal): Smallest change that solves the problem
- Agent 2 (Elegant): Clean abstraction, ideal architecture
- Agent 3 (Pragmatic): Balance between 1 and 2

Each agent returns: specific files to create/modify, line numbers, concrete approach.

After parallel design → present all 3 to user for selection.

---

### Phase 5: Implementation
**Goal:** Build the feature.

After user selects approach → implement.

Use TodoWrite to track progress.
Work systematically through the implementation plan.
Run tests as you go.

**Ask for confirmation before starting if anything is unclear.**

---

### Phase 6: Quality Review
**Goal:** Validate the implementation.

Launch 3 `code-reviewer` agents IN PARALLEL:
- Agent 1 (Simplicity): Is the code as simple as it needs to be? Rate 0-100.
- Agent 2 (Bugs): Are there any bugs, edge cases, or failure modes? Rate 0-100.
- Agent 3 (Conventions): Does it match project conventions and style? Rate 0-100.

Only report issues with confidence ≥ 80.
After review → fix what was found.

---

### Phase 7: Summary
**Goal:** Document what was done.

Provide:
- What was built
- Files changed
- How to test it
- Any known limitations

---

## Agent Definitions

### code-explorer
```
model: sonnet
color: yellow
tools: Glob, Grep, Read, BashOutput
```

### code-architect
```
model: sonnet
color: green
tools: Glob, Grep, Read, Write, BashOutput, TodoWrite
```

### code-reviewer
```
model: sonnet
color: red
tools: Glob, Grep, Read, BashOutput
confidence_threshold: 80
```

---

## Usage
/solana-feature-dev [optional feature description]

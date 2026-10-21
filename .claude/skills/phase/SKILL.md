---
name: phase
description: Start or continue a roadmap phase from docs/ROADMAP.md - plan, implement task by task, verify against the phase's Done-when criteria.
argument-hint: "[phase-number] [optional task focus]"
disable-model-invocation: true
---

Work on Phase $0 of @docs/ROADMAP.md. Extra focus from the user, if any: $ARGUMENTS

Current branch and state:
!`git status --short --branch`

## 1. Orient (read-only)
- Read the Phase $0 section: unchecked tasks and the **Done when** block.
- Use the Explore subagent to map the code those tasks touch. Keep raw file dumps out of this conversation.
- If you're not on a `phase-$0-*` branch, propose one and switch after I confirm.

## 2. Plan
Write a numbered plan covering the unchecked tasks only. For each step give: files touched,
the check that proves it works (test, command, output), and whether it calls an LLM (costs money).
Flag anything in the roadmap that seems wrong or underspecified, and ask me before inventing scope.
Stop and wait for my approval.

## 3. Implement, one task at a time
For each task:
1. Write or update the unit test first when the task is testable without an LLM.
2. Implement. Check the installed library version and docs before using LangChain/DeepEval APIs.
3. Run `uv run ruff check .` and `uv run pytest -m "not llm" -q`. Show the output.
4. Tick the task in docs/ROADMAP.md and commit (`git add` the specific files; imperative message).

## 4. Verify the phase
- Run each **Done when** check and paste the evidence (command + output). Ask me before any
  check that calls an LLM.
- Ask the `docs-verifier` subagent to check README/CLAUDE.md against the code if either changed.
- Ask the `eval-reviewer` subagent to review the phase diff (`git diff main...HEAD`) when the phase
  touched evaluation or policy code. Fix what affects correctness; list the rest as optional.
- Update the "Current phase" line and the Commands section of CLAUDE.md if they changed.

Finish with: what's done (with evidence), what's left, and the exact next command for me.

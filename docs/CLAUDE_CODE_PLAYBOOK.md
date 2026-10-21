# Claude Code playbook

How this repo is set up for Claude Code, and how to run the roadmap in `docs/ROADMAP.md` with it.

## How the setup is split

Claude does its best work when it (a) only has the context that matters for the current task,
(b) has a **check it can run** to know it's done, and (c) has **hard limits enforced by code** rather
than requests in prose.

| Need | Claude Code feature | In this repo |
|---|---|---|
| Rules Claude must always know | `CLAUDE.md` (loaded every session; keep it short) | `CLAUDE.md` |
| Rules for certain folders only | `.claude/rules/*.md` with `paths:` | `evals.md`, `agent.md`, `tests.md` |
| Workflows you repeat | Skills, called as `/name` | `/phase`, `/eval-run`, `/error-analysis`, `/add-eval-case`, `/readme-sync` |
| Heavy reading or an unbiased second opinion | Subagents (own context; only a summary comes back) | `docs-verifier`, `eval-reviewer`, `failure-analyst`, `test-writer` |
| Things that must happen every time | Hooks | ruff after every edit; Stop gate on lint and fast tests |
| Safety limits | Permission rules in `.claude/settings.json` | `.env` can't be read; eval runs and `git push` ask first; force-push denied |
| Current library docs | MCP server and the vendor skill | LangChain docs MCP (`.mcp.json`) and the DeepEval agent skill |
| Keep going until it's really done | `/goal <measurable condition>` | Each phase's "Done when" block in `docs/ROADMAP.md` |

All workflow skills use `disable-model-invocation: true`, so they run only when you type them.
Claude never starts a paid eval run on its own.

## One-time setup

1. **Install uv:** `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`. Restart the terminal
   afterwards. The hooks run through `uv`.
2. **Install pyright:** `npm install -g pyright`. Then, inside `claude`, run
   `/plugin install pyright-lsp@claude-plugins-official`.
3. **Install DeepEval's official agent skill:** `npx skills add confident-ai/deepeval --skill "deepeval"`.
   It's third-party code, so read what it installs.
4. **Add your OpenAI key:** copy `.env.example` to `.env` and set `OPENAI_API_KEY`.
5. **Check that everything loaded.** Start `claude` in the repo, then:
   - run `/context`: CLAUDE.md and the skills should be listed
   - run `/hooks`: there should be one PostToolUse hook and one Stop hook
   - run `/mcp`: approve `docs-langchain`

## Working habits

1. **One phase = one branch = fresh sessions.** Run `/clear` between unrelated tasks. Name sessions
   with `/rename`.
2. **Plan mode first for multi-file work.** Edit the plan before approving it. Skip planning for
   one-line fixes.
3. **Always give a check.** Say how "done" is proven (a test, a command, an output) and ask for the
   evidence.
4. **Two-strike rule.** After two corrections on the same thing, `/clear` and write a better first
   prompt.
5. **Writer ≠ reviewer.** Use `eval-reviewer`, the built-in `/code-review`, or a second session.
6. **Interview before big specs:** `Interview me with AskUserQuestion about <topic>; then update docs/ROADMAP.md`.
7. **Control cost.** Iterate with `--limit 2` and a cheap judge model. Run full evals only at the end
   of a step.
8. **Docs before APIs.** "Check the LangChain docs MCP / DeepEval skill and the installed version first."
9. **Every repeated mistake becomes a rule.** Add one line to CLAUDE.md or a rules file. If it must
   never happen, make it a hook or permission instead.

## What to type, phase by phase

The "Done when" block of each phase can be pasted into `/goal` after you've approved the plan. Add
"or stop after 30 turns".

- **Phase 1:** `/phase 1`, then `/readme-sync`, then `/code-review`.
- **Phase 2:**
  - Start with an interview about the case schema and categories, then `/clear`.
  - Run `/phase 2 reference date and structured Answer first`.
  - Have the `test-writer` subagent write tests for the loader and metrics.
  - Add cases with `/add-eval-case <scenario>`, one per category.
  - Finish with `/eval-run baseline-v1 --limit 5 --runs 1`.
- **Phase 3:**
  - Run `/phase 3`, writing `policy.py` test-first with `test-writer`.
  - Add an adversarial category with `/add-eval-case`.
  - Run `/eval-run v1-prompt-only`, then `/eval-run v2-code-guardrails`.
- **Phase 4:**
  - Run `/error-analysis`. You choose which root cause to fix.
  - Make one change per iteration, then run `/eval-run iter-N` with the baseline flags.
  - Compare a cheap model with a strong one.
- **Phase 5:** this can run in parallel with Phase 4 in a separate worktree session, since it touches
  `tests/`, `.github/` and `pyproject.toml`. Run `/phase 5`.
- **Phase 6:**
  - Run `/phase 6` and rewrite the README from code and `results/` only.
  - Then run `/readme-sync`.
  - In a brand-new session: "Pretend you're a hiring manager with 3 minutes; follow only the README and tell me where you got blocked."

## Things to avoid

- A CLAUDE.md that grows past about 100 lines. Move detail to rules files and skills.
- Adding agents or skills before you've typed the same thing three times.
- Letting Claude write the README "to look professional". It's written last, from code and results,
  and verified.
- Bypass-permissions mode. Auto mode plus the allowlist is fast enough and safe.
- Trusting a single eval run.

## Sources
[Best practices](https://code.claude.com/docs/en/best-practices) ·
[Skills](https://code.claude.com/docs/en/skills) · [Subagents](https://code.claude.com/docs/en/sub-agents) ·
[Hooks](https://code.claude.com/docs/en/hooks) · [/goal](https://code.claude.com/docs/en/goal) ·
[Memory & rules](https://code.claude.com/docs/en/memory) ·
[Extend Claude Code](https://code.claude.com/docs/en/features-overview) ·
[Code intelligence](https://code.claude.com/docs/en/plugins/code-intelligence) ·
[LangChain docs MCP](https://docs.langchain.com/use-these-docs) ·
[DeepEval agent skill](https://deepeval.com/docs/vibe-coder-quickstart)

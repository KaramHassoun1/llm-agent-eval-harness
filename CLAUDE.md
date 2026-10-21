# Refund Agent — evaluation-driven LLM agent

A LangChain refund-support agent plus a reproducible evaluation harness (DeepEval + code-based checks).
The goal of this repo is a portfolio piece: honest, reproducible, measurably improved. The roadmap
and acceptance criteria live in @docs/ROADMAP.md — read the current phase there before planning work.

## Commands (Windows + uv; run from repo root)
- Install: `uv sync --dev`
- Lint/format: `uv run ruff check . --fix` and `uv run ruff format .`
- Types: `uv run mypy src`
- Fast tests (no API calls, no cost): `uv run pytest -q` (the `llm` marker is excluded by default)
- Eval smoke run (costs money, 2 cases): `uv run refund-eval --limit 2 --out results/<label>.json`
- Full eval (costs money): `uv run refund-eval --runs 3` — ASK before running this
- Terminal chat with the agent: `uv run python -m refund_agent`

## Layout
- `src/refund_agent/` agent factory, tools, data, prompts, schemas, config (policy.py arrives in Phase 3)
- `src/refund_eval/` dataset, DeepEval metrics, runner, JSON report, `refund-eval` CLI
- `tests/` fast unit tests · `examples/metric_basics/` toy metric demos
- Planned: `evals/cases/*.yaml` (Phase 2) · `results/` saved runs · `docs/EXPERIMENTS.md` (Phase 4)

## Rules
- IMPORTANT: The README and docs may only describe what exists in the code. Every command, path,
  number and threshold in them must be verified against the code before you write it.
- Never call an LLM in unit tests. Tests that need an API key get `@pytest.mark.llm`.
- Never run the full eval without asking; use `--limit` while iterating. LLM calls cost real money.
- Business rules (eligibility, amounts, double refunds) are enforced in `policy.py`, not only in prompts.
- "Today" is injected from config (`REFERENCE_DATE`); never call `date.today()` in agent or eval code.
- LangChain 1.x and DeepEval APIs change fast. Before using an API, check the installed version
  (`uv pip show langchain deepeval`) and the docs (LangChain docs MCP server / DeepEval skill).
  Do not write APIs from memory.
- Never read or print `.env`. Keys come from environment variables.
- Settings live in one place: `src/refund_agent/config.py`. No model names or thresholds elsewhere.

## Git
- One branch per phase: `phase-<n>-<slug>`. Small commits, imperative messages.
- Never force-push. Never commit `results/` files larger than 1 MB.

## When compacting
Preserve: the current phase and task, the list of modified files, the last test/eval command run
and its result, and any open decisions.

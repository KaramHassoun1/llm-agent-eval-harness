# Roadmap

Each phase lists tasks and a **Done when** block. The Done-when lines are written so they can be pasted
into `/goal` and checked from command output. Tick tasks (`[x]`) as they land.

Current phase: **1**

## Phase 1 — Honest and runnable
- [x] Move code into `src/refund_agent/` and `src/refund_eval/`; remove every `sys.path` hack
- [x] One `config.py` (pydantic-settings): agent model, judge model, `REFERENCE_DATE`, thresholds
- [x] `pyproject.toml`: real description, drop `asyncio`, add `python-dotenv`, `pydantic-settings`;
      dev group `pytest`, `ruff`, `mypy`. (`streamlit` extra deferred to Phase 6: nothing uses it yet.)
- [x] CLI entry point `refund-eval` (`--limit`, `--runs`, `--model`, `--judge-model`, `--out`)
- [x] Move `understanding_metrics/` to `examples/`, credit the DeepEval docs, fix `asnwer_` typo
- [x] Delete commented-out debug code; fix typos in prompts and names
- [x] Fix the unused/reset `test_cases` bug in the old tool-correctness script (or delete the script)
- [x] Add a LICENSE (MIT)
- [x] `.gitignore` covers `.env`, caches and local Claude settings
- [x] Rewrite README *only* to match current code (minimal; full rewrite is Phase 6)

**Done when:** `uv sync --dev` succeeds; `uv run ruff check .` exits 0;
`uv run refund-eval --help` prints usage; `uv run refund-eval --limit 1 --runs 1` completes;
`grep -rn "sys.path" src` returns nothing; every path and command in README exists/works.

## Phase 2 — Trustworthy evaluation
- [ ] Inject "today" via config into the date tool; purchases defined as `days_ago` relative to it
- [ ] Extend `Answer`: `decision` (refunded | denied | need_info | info_only), `refund_amount`,
      `ticket_issued`
- [ ] Cases in `evals/cases/*.yaml` with `id`, `category`, `input`, expected `decision`,
      `refund_amount`, `ticket_issued`, `forbidden_tools`, optional `expected_tools`
- [ ] 30–40 cases across: happy path, partial, expired, boundary 30/31 days, future-dated,
      unknown user, unknown item, missing username, info-only, duplicate request,
      multi-turn, prompt injection / policy bypass
- [ ] Code-based metrics: decision, exact amount, ticket issued, forbidden tool not called
- [ ] DeepEval metrics kept for language/plan quality only
- [ ] Repeat runs (`--runs N`): mean, std, pass^k per metric and per category
- [ ] Judge validation: hand labels in `evals/labels.yaml`; report judge–human agreement
- [ ] Every run saved to `results/<timestamp>.json` with git sha, models, prompt hash,
      reference date, scores, tokens, cost, latency

**Done when:** `uv run pytest -m "not llm" -q` passes; dataset has ≥30 cases in ≥10 categories;
two consecutive `--limit 5 --runs 1` runs give identical code-based decision results for the
same model; a results JSON contains all metadata fields above.

## Phase 3 — Guardrails in code
- [ ] `policy.py`: `check_eligibility(user, items, today) -> list[ItemDecision]` (pure, unit-tested)
- [ ] `issue_refund_ticket` recomputes amount server-side; ignores model-supplied amount;
      rejects ineligible, unknown, already-refunded items
- [ ] Idempotency store for issued refunds (in-memory, resettable per eval case)
- [ ] Human-handoff above `MAX_AUTO_REFUND` via LangGraph interrupt
- [ ] All tools return Pydantic models (no mixed str/dict)
- [ ] Prompt version tag: `v1-prompt-only` vs `v2-code-guardrails`, selectable from CLI

**Done when:** policy unit tests cover every boundary (29/30/31 days, future, unknown, duplicate)
and pass; full eval run for v1 and v2 saved in `results/`; on the adversarial category v2 issues
zero tickets that the policy forbids.

## Phase 4 — Improvement story
- [ ] Baseline run saved and tagged
- [ ] Every failure classified as agent bug / dataset bug / judge bug in `docs/EXPERIMENTS.md`
- [ ] Explain the plan-quality score (agent never plans? metric not applicable?) with evidence
- [ ] At least 3 change → re-run iterations, each with a before/after table
- [ ] Model comparison (cheap vs strong): accuracy, cost per conversation, p50/p95 latency

**Done when:** `docs/EXPERIMENTS.md` has a baseline table, ≥3 iteration tables, a model comparison
table, and every number links to a file in `results/`.

## Phase 5 — Engineering quality
- [ ] Unit tests for tools, policy, code-based metrics, dataset loader (no API calls)
- [ ] GitHub Actions `ci.yml`: ruff, mypy, pytest `-m "not llm"` on push/PR
- [ ] GitHub Actions `eval.yml`: manual/nightly, uses `OPENAI_API_KEY` secret, uploads report,
      fails if code-based pass rate drops below `evals/baseline.json`
- [ ] pre-commit config (ruff, ruff-format)

**Done when:** `uv run mypy src` exits 0; `uv run pytest -m "not llm" --cov=src` ≥ 80% on
`policy.py` and metrics; `ci.yml` passes on GitHub.

## Phase 6 — Presentation
- [ ] Streamlit app: chat, live tool-call trace, policy decisions, results tab from `results/`
- [ ] Deploy (Hugging Face Spaces or Streamlit Cloud), bring-your-own-key or rate-limited
- [ ] README rewritten from the working code: pitch, GIF, diagram, headline results,
      how to run, how to adapt, limitations
- [ ] Blog/LinkedIn write-up of the main finding

**Done when:** the docs-verifier agent reports zero mismatches between README and code; the
demo URL loads; a fresh clone following the README reaches a successful `--limit 1` run.

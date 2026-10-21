---
paths:
  - "src/refund_eval/**"
  - "evals/**"
  - "results/**"
---

# Evaluation rules

- A case is YAML in `evals/cases/<category>.yaml` with: `id`, `category`, `input` (string or list of
  turns), `expected.decision`, `expected.refund_amount` (number or null), `expected.ticket_issued`,
  `forbidden_tools`, optional `expected_tools`, optional `notes`. IDs are stable; never renumber.
- Expected outcomes must follow from `policy.py` + the purchase data at `REFERENCE_DATE`. If they
  disagree, the case is wrong or the policy is wrong — say which; never tweak a case to make a run pass.
- Prefer code-based metrics (exact decision, amount, ticket, forbidden tools). Use an LLM judge only
  for what code can't check (tone, explanation quality, plan quality). Pin the judge model in config.
- Report per-metric and per-category: mean, std across runs, pass rate, pass^k. Never report one run
  as a result.
- Every saved run includes git sha, agent model, judge model, prompt version + hash, reference date,
  number of runs, token usage, cost estimate, latency. A number without this metadata is not a result.
- Keep thresholds in config only.

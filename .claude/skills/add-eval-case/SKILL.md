---
name: add-eval-case
description: Add evaluation cases for a scenario to evals/cases, with expected outcomes derived from policy.py, then run just those cases.
argument-hint: "<scenario description>"
disable-model-invocation: true
---

Add eval cases for this scenario: $ARGUMENTS

1. Pick the category file in `evals/cases/` (create one if no category fits, and say so).
2. Write 1–3 cases (the main case plus its nearest boundary) in the existing YAML schema.
   Use purchase data relative to `REFERENCE_DATE`; add purchases to the fixture data if needed.
3. Derive every expected field by calling the policy functions, not by reasoning about them:
   `uv run python -c "from refund_agent.policy import ...; print(...)"`. Paste that output.
4. Check that the new IDs are unique and the loader accepts them: `uv run pytest tests/test_dataset.py -q`.
5. Ask before running them against the model, then run `uv run refund-eval --only <ids> --runs 1`.

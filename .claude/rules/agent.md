---
paths:
  - "src/refund_agent/**"
---

# Agent rules

- `policy.py` holds pure functions with no LangChain or I/O imports, so they are unit-testable.
  Tools call policy; tools never re-implement a rule.
- Tools take and return Pydantic models. No tool returns a bare `str` or an ad-hoc `dict`.
- A tool that moves money (`issue_refund_ticket`) never trusts amounts or eligibility from the model:
  it recomputes from item names via `policy.py` and refuses anything the policy rejects.
- The system prompt explains the policy to the model, but code enforces it. Changing a prompt is a
  new prompt version (`prompts/v<n>-<slug>.md`); keep old versions so runs stay comparable.
- No `date.today()`, no model names, no thresholds in this package outside `config.py`.

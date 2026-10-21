---
paths:
  - "tests/**"
---

# Test rules

- Unit tests never call an LLM or the network. Anything that does is marked `@pytest.mark.llm`
  and lives in `tests/llm/`.
- Test behaviour through public functions; one behaviour per test; names read as sentences
  (`test_refund_denied_when_purchase_is_31_days_old`).
- Boundaries are explicit: 29, 30 and 31 days; today; tomorrow; unknown user; unknown item;
  duplicate refund.
- Fix the code, not the test, unless the test encodes a wrong expectation — and say so.

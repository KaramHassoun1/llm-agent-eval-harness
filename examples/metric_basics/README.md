# Metric basics

Small, self-contained scripts that show each DeepEval agent metric on a toy multiplication agent,
with no refund logic. They follow the examples in the [DeepEval documentation](https://deepeval.com/docs/metrics-introduction)
and are kept here as a learning reference; the refund evaluation lives in `src/refund_eval/`.

Run one from the repository root (needs `OPENAI_API_KEY`; each run makes paid API calls):

```bash
uv run --env-file .env python examples/metric_basics/tool_correctness.py
```

The scripts pick their own models (`gpt-4`, `gpt-4o`, `gpt-4o-mini`) instead of using
`src/refund_agent/config.py`.

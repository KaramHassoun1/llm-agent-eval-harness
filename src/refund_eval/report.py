"""Turn DeepEval results into a JSON-serialisable run record."""

import subprocess
from datetime import UTC, datetime
from typing import Any

from deepeval.evaluate.types import EvaluationResult

from refund_agent.config import Settings


def git_sha() -> str | None:
    try:
        result = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True)
    except FileNotFoundError:
        return None
    return result.stdout.strip() or None


def case_records(result: EvaluationResult) -> list[dict[str, Any]]:
    return [
        {
            "input": test.input,
            "success": test.success,
            "metrics": [
                {
                    "name": m.name,
                    "score": m.score,
                    "threshold": m.threshold,
                    "success": m.success,
                    "reason": m.reason,
                    "error": m.error,
                }
                for m in test.metrics_data or []
            ],
        }
        for test in result.test_results
    ]


def build_run_record(
    settings: Settings,
    runs: list[tuple[EvaluationResult, EvaluationResult]],
    limit: int | None,
) -> dict[str, Any]:
    return {
        "created_at": datetime.now(UTC).isoformat(),
        "git_sha": git_sha(),
        "agent_model": settings.agent_model,
        "judge_model": settings.judge_model,
        "reference_date": settings.today().isoformat(),
        "limit": limit,
        "runs": [
            {"trace_metrics": case_records(trace), "single_turn_metrics": case_records(single)}
            for trace, single in runs
        ],
    }

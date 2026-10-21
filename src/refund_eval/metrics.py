from deepeval.metrics import (
    ArgumentCorrectnessMetric,
    BaseMetric,
    GEval,
    PlanAdherenceMetric,
    PlanQualityMetric,
    StepEfficiencyMetric,
    TaskCompletionMetric,
    ToolCorrectnessMetric,
)
from deepeval.test_case import SingleTurnParams, ToolCallParams

from refund_agent.config import Settings

SUCCESSFUL_TASK_DESCRIPTION = """
If the username is missing, ask the user to provide it.
For a refund request, identify the customer and the requested purchases, and
check that each purchase is no more than 30 days old and is not in the future.
Refund only the items requested by the user. If the customer or requested item
cannot be found, do not issue a refund ticket and explain why.
Once the necessary information is available, tell the user whether a refund
ticket was issued and its amount, or explain why no refund was issued.
For an information-only request, answer the question without issuing a ticket.
"""


def build_trace_metrics(settings: Settings) -> list[BaseMetric]:
    """Metrics scored from the execution trace captured by DeepEval's CallbackHandler."""
    judge, t = settings.judge_model, settings.thresholds
    return [
        TaskCompletionMetric(
            threshold=t.task_completion,
            model=judge,
            task=SUCCESSFUL_TASK_DESCRIPTION,
            include_reason=True,
        ),
        StepEfficiencyMetric(threshold=t.step_efficiency, model=judge, include_reason=True),
        PlanQualityMetric(threshold=t.plan_quality, model=judge, include_reason=True),
        PlanAdherenceMetric(threshold=t.plan_adherence, model=judge, include_reason=True),
    ]


def build_single_turn_metrics(settings: Settings) -> list[BaseMetric]:
    """Metrics scored from an LLMTestCase built from the same agent run."""
    judge, t = settings.judge_model, settings.thresholds
    return [
        ArgumentCorrectnessMetric(
            threshold=t.argument_correctness, model=judge, include_reason=True
        ),
        ToolCorrectnessMetric(
            threshold=t.tool_correctness,
            model=judge,
            include_reason=True,
            evaluation_params=[ToolCallParams.INPUT_PARAMETERS],
        ),
        GEval(
            name="Answer Correctness",
            evaluation_params=[
                SingleTurnParams.INPUT,
                SingleTurnParams.ACTUAL_OUTPUT,
                SingleTurnParams.EXPECTED_OUTPUT,
            ],
            evaluation_steps=[
                "Check that the actual output and expected output have the same "
                "logical conclusion about the user's request.",
            ],
            threshold=t.answer_correctness,
            model=judge,
            verbose_mode=True,
        ),
    ]

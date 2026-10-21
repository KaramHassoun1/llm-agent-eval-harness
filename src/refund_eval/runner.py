"""Run the refund agent over the dataset and score it with all seven metrics.

Each run has two stages that share one agent response per case:
1. `evals_iterator` scores four trace metrics from the CallbackHandler trace.
2. `evaluate` scores three single-turn metrics from an LLMTestCase built from that response.
"""

from collections.abc import Iterator
from uuid import uuid4

from deepeval.dataset import Golden
from deepeval.evaluate import CacheConfig, DisplayConfig, evaluate
from deepeval.evaluate.types import EvaluationResult
from deepeval.integrations.langchain import CallbackHandler
from deepeval.test_case import LLMTestCase, ToolCall

from refund_agent.agent import build_agent
from refund_agent.config import Settings
from refund_eval.dataset import build_dataset
from refund_eval.metrics import build_single_turn_metrics, build_trace_metrics


def tools_called(response: dict) -> list[ToolCall]:
    return [
        ToolCall(name=call["name"], input_parameters=call["args"])
        for message in response["messages"]
        for call in getattr(message, "tool_calls", None) or []
    ]


def run_once(settings: Settings, limit: int | None) -> tuple[EvaluationResult, EvaluationResult]:
    """One pass over the dataset. Returns (trace-metric results, single-turn results)."""
    agent = build_agent(settings)
    cache_config = CacheConfig(use_cache=False, write_cache=False)
    display_config = DisplayConfig(inspect_after_run=False)
    test_cases = []

    # Drive the generator by hand: its return value carries the trace-metric results.
    goldens: Iterator[Golden] = build_dataset(limit).evals_iterator(
        metrics=build_trace_metrics(settings),
        cache_config=cache_config,
        display_config=display_config,
    )
    while True:
        try:
            golden = next(goldens)
        except StopIteration as done:
            trace_result: EvaluationResult = done.value
            break

        response = agent.invoke(
            {"messages": [{"role": "user", "content": golden.input}]},
            config={
                "configurable": {"thread_id": str(uuid4())},
                "callbacks": [CallbackHandler()],
            },
        )
        test_cases.append(
            LLMTestCase(
                input=golden.input,
                actual_output=response["structured_response"].answer,
                expected_output=golden.expected_output,
                tools_called=tools_called(response),
                expected_tools=golden.expected_tools,
            )
        )

    single_turn_result = evaluate(
        test_cases=test_cases,
        metrics=build_single_turn_metrics(settings),
        cache_config=cache_config,
        display_config=display_config,
    )
    return trace_result, single_turn_result

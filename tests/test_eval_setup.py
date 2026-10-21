import pytest

from refund_agent.agent import build_agent
from refund_agent.config import get_settings
from refund_eval.cli import parse_args
from refund_eval.dataset import GOLDENS, build_dataset
from refund_eval.metrics import build_single_turn_metrics, build_trace_metrics


def test_dataset_has_seven_cases_and_limit_takes_the_first_n():
    assert len(build_dataset().goldens) == len(GOLDENS) == 7
    assert [g.input for g in build_dataset(2).goldens] == [g.input for g in GOLDENS[:2]]


def test_metrics_use_thresholds_from_config(monkeypatch):
    monkeypatch.setenv("REFUND_THRESHOLDS__PLAN_QUALITY", "0.3")
    settings = get_settings()
    trace = build_trace_metrics(settings)
    single = build_single_turn_metrics(settings)
    assert len(trace) == 4 and len(single) == 3
    assert [m.threshold for m in trace] == [0.8, 0.8, 0.3, 0.8]
    assert [m.threshold for m in single] == [0.8, 0.9, 0.8]


def test_agent_builds_without_calling_the_api():
    assert build_agent() is not None


def test_cli_help_exits_cleanly(capsys):
    with pytest.raises(SystemExit) as exit_info:
        parse_args(["--help"])
    assert exit_info.value.code == 0
    assert "--limit" in capsys.readouterr().out


@pytest.mark.parametrize("flag", ["--runs", "--limit"])
def test_cli_rejects_non_positive_counts(flag):
    with pytest.raises(SystemExit) as exit_info:
        parse_args([flag, "0"])
    assert exit_info.value.code == 2

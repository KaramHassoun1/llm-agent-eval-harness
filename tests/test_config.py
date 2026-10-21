from datetime import date

from refund_agent.config import Settings, get_settings


def test_defaults_match_the_documented_thresholds():
    t = get_settings().thresholds
    assert t.tool_correctness == 0.9
    assert {t.task_completion, t.argument_correctness, t.answer_correctness} == {0.8}


def test_environment_variables_override_settings(monkeypatch):
    monkeypatch.setenv("REFUND_AGENT_MODEL", "some-other-model")
    monkeypatch.setenv("REFUND_THRESHOLDS__TOOL_CORRECTNESS", "0.5")
    settings = get_settings()
    assert settings.agent_model == "some-other-model"
    assert settings.thresholds.tool_correctness == 0.5


def test_today_uses_reference_date_when_set():
    assert Settings(reference_date=date(2026, 10, 15)).today() == date(2026, 10, 15)


def test_today_falls_back_to_the_real_date():
    assert Settings().today() == date.today()

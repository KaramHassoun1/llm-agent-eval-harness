import pytest


@pytest.fixture(autouse=True)
def isolated_settings(monkeypatch, tmp_path):
    """Keep the developer's .env and REFUND_* variables out of unit tests."""
    monkeypatch.chdir(tmp_path)
    for name in ["REFUND_AGENT_MODEL", "REFUND_JUDGE_MODEL", "REFUND_REFERENCE_DATE"]:
        monkeypatch.delenv(name, raising=False)
    # Model clients need a key to construct; no test makes a network call.
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-not-used")

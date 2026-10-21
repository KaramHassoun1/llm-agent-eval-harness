"""All tunable settings in one place.

Override any field with a `REFUND_`-prefixed environment variable or a line in `.env`,
for example `REFUND_AGENT_MODEL=gpt-5-mini` or `REFUND_THRESHOLDS__TOOL_CORRECTNESS=0.8`.
"""

from datetime import date

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Thresholds(BaseModel):
    """Pass marks (0-1) for the seven evaluation metrics."""

    task_completion: float = 0.8
    step_efficiency: float = 0.8
    plan_quality: float = 0.8
    plan_adherence: float = 0.8
    argument_correctness: float = 0.8
    tool_correctness: float = 0.9
    answer_correctness: float = 0.8


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="REFUND_",
        env_file=".env",
        env_nested_delimiter="__",
        extra="ignore",
    )

    agent_model: str = "gpt-6-luna"
    judge_model: str = "gpt-6-luna"
    # Fixed "today" for reproducible runs; None means the real current date.
    reference_date: date | None = None
    thresholds: Thresholds = Thresholds()

    def today(self) -> date:
        return self.reference_date or date.today()


def get_settings() -> Settings:
    return Settings()

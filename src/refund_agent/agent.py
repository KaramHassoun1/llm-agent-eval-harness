from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver

from refund_agent.config import Settings, get_settings
from refund_agent.prompts import AGENT_SYSTEM_PROMPT
from refund_agent.schemas import Answer
from refund_agent.tools import TOOLS


def build_agent(settings: Settings | None = None):
    """Create the refund agent. Needs OPENAI_API_KEY in the environment."""
    settings = settings or get_settings()
    return create_agent(
        model=init_chat_model(model=settings.agent_model),
        system_prompt=AGENT_SYSTEM_PROMPT,
        tools=TOOLS,
        response_format=Answer,
        checkpointer=InMemorySaver(),
    )

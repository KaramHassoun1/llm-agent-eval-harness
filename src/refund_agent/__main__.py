"""Interactive refund conversation in the terminal: `uv run python -m refund_agent`."""

from uuid import uuid4

from dotenv import load_dotenv
from langchain.messages import HumanMessage

from refund_agent.agent import build_agent


def run_conversation() -> None:
    agent = build_agent()
    config = {"configurable": {"thread_id": str(uuid4())}}

    text = "I would like to request a refund"
    print(text)
    question = HumanMessage(content=text)

    conversation = True
    while conversation:
        response = agent.invoke({"messages": question}, config=config)
        structured_response = response["structured_response"]
        print(structured_response.answer)

        conversation = structured_response.conversation
        if conversation:
            question = HumanMessage(content=input("reply: \n"))

    print("the job is done!")


if __name__ == "__main__":
    load_dotenv()
    run_conversation()

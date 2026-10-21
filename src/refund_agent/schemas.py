from pydantic import BaseModel, Field


class Answer(BaseModel):
    answer: str = Field(description="The reply to the user's message.")
    conversation: bool = Field(
        default=True,
        description=(
            "Whether the conversation should continue. False once the agent has made the "
            "refund decision; True if it still needs more information from the user."
        ),
    )


class PurchaseItem(BaseModel):
    name: str = Field(description="Name of the purchased item.")

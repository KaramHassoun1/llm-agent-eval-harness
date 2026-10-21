import logging

from langchain.tools import tool

from refund_agent.config import get_settings
from refund_agent.data import users_data
from refund_agent.schemas import PurchaseItem

logger = logging.getLogger(__name__)

USER_NOT_FOUND = {"status": "there was no username found"}


@tool
def get_user_purchase_history(user: str) -> dict:
    """Take the customer's username and return their purchase history, if the user exists."""
    logger.info("get_user_purchase_history: user=%s", user)
    return users_data.get(user, USER_NOT_FOUND)


@tool
def calculate_right_refund(user: str, items: list[PurchaseItem]) -> str | dict:
    """Take the username and the list of items to return, and return the refund's total value."""
    logger.info("calculate_right_refund: user=%s", user)
    purchases = users_data.get(user)
    if not purchases:
        return USER_NOT_FOUND

    total_refund = sum(purchases[item.name]["price"] for item in items if item.name in purchases)
    return f"the value of the refund is: {total_refund}"


@tool
def issue_refund_ticket(user: str, refund_amount: int) -> str:
    """Send a ticket to the right team to pay the refund."""
    logger.info("issue_refund_ticket: user=%s amount=%s", user, refund_amount)
    return f"a refund ticket has been issued successfully with the amount of {refund_amount}"


@tool
def get_today_date() -> str:
    """Return today's date in YYYY-MM-DD format.
    This tool takes no arguments.
    Only use it if the user exists and an item is present for refund."""
    logger.info("get_today_date")
    return get_settings().today().isoformat()


TOOLS = [calculate_right_refund, get_user_purchase_history, issue_refund_ticket, get_today_date]

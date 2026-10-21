from refund_agent.tools import (
    calculate_right_refund,
    get_today_date,
    get_user_purchase_history,
    issue_refund_ticket,
)


def test_purchase_history_of_known_user():
    history = get_user_purchase_history.invoke({"user": "user123"})
    assert set(history) == {"book", "pen"}


def test_purchase_history_of_unknown_user_reports_not_found():
    assert get_user_purchase_history.invoke({"user": "user999"}) == {
        "status": "there was no username found"
    }


def test_refund_adds_prices_of_requested_items_only():
    result = calculate_right_refund.invoke({"user": "user123", "items": [{"name": "book"}]})
    assert result == "the value of the refund is: 23"


def test_refund_ignores_items_the_user_did_not_buy():
    items = [{"name": "book"}, {"name": "pen"}, {"name": "sneakers"}]
    result = calculate_right_refund.invoke({"user": "user123", "items": items})
    assert result == "the value of the refund is: 30"


def test_refund_for_unknown_user_reports_not_found():
    result = calculate_right_refund.invoke({"user": "user999", "items": [{"name": "book"}]})
    assert result == {"status": "there was no username found"}


def test_ticket_confirms_the_amount():
    assert "45" in issue_refund_ticket.invoke({"user": "user126", "refund_amount": 45})


def test_date_tool_uses_the_configured_reference_date(monkeypatch):
    monkeypatch.setenv("REFUND_REFERENCE_DATE", "2026-10-15")
    assert get_today_date.invoke({}) == "2026-10-15"

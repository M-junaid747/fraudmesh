from app.rules import evaluate_rules


def test_high_amount_flagged():
    flagged, reason = evaluate_rules(6000, None)
    assert flagged is True
    assert "amount" in reason


def test_normal_amount_not_flagged():
    flagged, reason = evaluate_rules(100, "device-123")
    assert flagged is False
    assert reason is None


def test_unknown_device_flagged():
    flagged, reason = evaluate_rules(50, "unknown-device-1")
    assert flagged is True
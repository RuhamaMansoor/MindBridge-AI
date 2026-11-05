
from safety_guardian import SafetyLevel, assess_safety


def test_normal_message():
    result = assess_safety(
        crisis_detected=False,
        uncertain=False,
        persistent_distress=False,
    )
    assert result.level == SafetyLevel.NORMAL
    assert result.requires_professional_help is False


def test_persistent_distress():
    result = assess_safety(
        crisis_detected=False,
        persistent_distress=True,
    )
    assert result.level == SafetyLevel.REVIEW
    assert result.requires_professional_help is True


def test_uncertain_assessment():
    result = assess_safety(
        crisis_detected=False,
        uncertain=True,
    )
    assert result.level == SafetyLevel.REVIEW


def test_crisis_has_highest_priority():
    result = assess_safety(
        crisis_detected=True,
        uncertain=True,
        persistent_distress=True,
    )
    assert result.level == SafetyLevel.CRISIS


def test_rule_based_crisis():
    result = assess_safety(
        crisis_detected=False,
        rule_crisis_detected=True,
    )
    assert result.level == SafetyLevel.CRISIS


def test_assessment_failure():
    result = assess_safety(
        crisis_detected=False,
        assessment_failed=True,
    )
    assert result.level == SafetyLevel.REVIEW
    assert result.requires_professional_help is True

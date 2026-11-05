
"""
MindBridge AI - Medical Safety Guardian Tests
Version: 0.3.0

Automated regression tests for configured
medical emergency warning signs.

Passing tests do not establish clinical safety.
"""

import pytest

from medical_safety_guardian import (
    MedicalSafetyResult,
    assess_medical_safety,
)


# ============================================================
# 1. EMERGENCY RED FLAGS
# ============================================================

@pytest.mark.parametrize(
    "message",
    [
        "I have sudden vision loss in one eye.",
        "I have severe eye pain.",
        "I have sudden face drooping.",
        "Meri nazar achanak kam ho gayi hai.",
        "Meri aankh mein bohat tez dard hai.",
        (
            "Mere seene mein achanak bohat tez "
            "dard hai aur saans lene mein mushkil hai."
        ),
        "میری نظر اچانک کم ہو گئی ہے۔",
        "میری آنکھ میں شدید درد ہے۔",
    ],
)
def test_emergency_red_flags(message):
    result = assess_medical_safety(message)

    assert isinstance(result, MedicalSafetyResult)
    assert result.emergency_detected is True
    assert result.category is not None
    assert result.uncertain is False


# ============================================================
# 2. NORMAL MESSAGES
# ============================================================

@pytest.mark.parametrize(
    "message",
    [
        "I am feeling stressed at work.",
        "Mujhe office ka stress hai.",
        "مجھے دفتر کے کام کا دباؤ ہے۔",
        "I want to improve my sleep.",
    ],
)
def test_normal_messages(message):
    result = assess_medical_safety(message)

    assert result.emergency_detected is False


# ============================================================
# 3. HYPOTHETICAL AND NEGATED STATEMENTS
# ============================================================

@pytest.mark.parametrize(
    "message",
    [
        "What if someone has severe eye pain?",
        "Agar kisi ko seene mein dard ho?",
        "I do not have chest pain.",
    ],
)
def test_contextual_review(message):
    result = assess_medical_safety(message)

    assert result.emergency_detected is False
    assert result.uncertain is True


# ============================================================
# 4. MIXED NEGATION REGRESSION TESTS
# ============================================================

@pytest.mark.parametrize(
    "message",
    [
        (
            "I do not have chest pain, "
            "but I have sudden vision loss."
        ),
        (
            "Mujhe seene mein dard nahi hai "
            "lekin meri nazar achanak chali gayi hai."
        ),
        (
            "I have no chest pain, "
            "but I have severe eye pain."
        ),
    ],
)
def test_negation_does_not_hide_other_emergencies(
    message,
):
    result = assess_medical_safety(message)

    assert result.emergency_detected is True
    assert result.category in {
        "sudden_vision_loss",
        "severe_eye_pain",
    }
    assert result.uncertain is False


# ============================================================
# 5. CARDIORESPIRATORY EMERGENCY
# ============================================================

def test_chest_pain_with_breathing_difficulty():
    result = assess_medical_safety(
        "I have chest pain and cannot breathe."
    )

    assert result.emergency_detected is True
    assert (
        result.category
        == "cardiorespiratory_emergency"
    )
    assert result.uncertain is False


# ============================================================
# 6. HYPOTHETICAL QUESTION
# ============================================================

def test_hypothetical_question_requires_review():
    result = assess_medical_safety(
        "What if someone has chest pain?"
    )

    assert result.emergency_detected is False
    assert result.uncertain is True


# ============================================================
# 7. INVALID INPUT
# ============================================================

def test_invalid_input():
    with pytest.raises(TypeError):
        assess_medical_safety(None)


# ============================================================
# 8. EMPTY MESSAGE
# ============================================================

def test_empty_message():
    result = assess_medical_safety("")

    assert result.emergency_detected is False
    assert result.category is None


# ============================================================
# 9. RESULT STRUCTURE
# ============================================================

def test_result_structure():
    result = assess_medical_safety(
        "I have severe eye pain."
    )

    assert isinstance(
        result.emergency_detected,
        bool,
    )
    assert isinstance(result.reason, str)
    assert isinstance(result.uncertain, bool)
    assert result.category == "severe_eye_pain"


# ============================================================
# 10. SAME-CLAUSE NEGATION
# ============================================================

def test_same_clause_negation():
    result = assess_medical_safety(
        "I have no chest pain and sudden vision loss."
    )

    assert result.emergency_detected is True
    assert result.category == "sudden_vision_loss"
    assert result.uncertain is False


# ============================================================
# 11. HISTORICAL SYMPTOMS
# ============================================================

def test_historical_chest_pain():
    result = assess_medical_safety(
        "I had chest pain last year, but I am fine now."
    )

    assert result.emergency_detected is False
    assert result.uncertain is True


# ============================================================
# 12. URDU NEGATION WITH ACTIVE EMERGENCY
# ============================================================

def test_urdu_negation_with_vision_loss():
    result = assess_medical_safety(
        "مجھے سینے میں درد نہیں ہے "
        "لیکن اچانک نظر چلی گئی ہے۔"
    )

    assert result.emergency_detected is True
    assert result.category == "sudden_vision_loss"


# ============================================================
# 13. THIRD-PERSON STROKE WARNING
# ============================================================

@pytest.mark.parametrize(
    "message",
    [
        "My father suddenly cannot speak properly.",
        "My mother suddenly can't talk properly.",
        "My brother has slurred speech.",
    ],
)
def test_stroke_speech_warnings(message):
    result = assess_medical_safety(message)

    assert result.emergency_detected is True
    assert result.category == "stroke_warning"
    assert result.uncertain is False


# ============================================================
# 14. DENIED CHEST PAIN WITH BREATHING EMERGENCY
# ============================================================

def test_denied_chest_pain_with_breathing_emergency():
    result = assess_medical_safety(
        "I have no chest pain but "
        "I suddenly cannot breathe."
    )

    assert result.emergency_detected is True
    assert result.category == "breathing_difficulty"


# ============================================================
# 15. MIXED SYMPTOMS IN ROMAN URDU
# ============================================================

def test_roman_urdu_mixed_symptoms():
    result = assess_medical_safety(
        "Mujhe seene mein dard nahi hai "
        "aur meri nazar achanak kam ho gayi hai."
    )

    assert result.emergency_detected is True
    assert result.category == "sudden_vision_loss"

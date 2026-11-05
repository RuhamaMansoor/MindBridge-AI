
"""
MindBridge AI - Combined Emergency Regression Tests

Tests:
1. Combined mental-health and medical emergency
2. Mental-health crisis only
3. Medical emergency only
4. Medical emergency when AWS assessment fails
5. Localized emergency responses

All tests use mocks.
No real AWS or OpenAI API calls.
"""

from types import SimpleNamespace
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

import main
from safety_guardian import SafetyLevel


client = TestClient(main.app)


def fake_safety(level):
    return SimpleNamespace(
        level=level,
        reason="Test safety assessment",
        requires_professional_help=False,
    )


def fake_medical(emergency=False, category=None):
    return SimpleNamespace(
        emergency_detected=emergency,
        category=category,
        reason="Test medical assessment",
        uncertain=False,
    )


def post_chat(message, language="en"):
    return client.post(
        "/chat",
        json={
            "message": message,
            "language_mode": "manual",
            "preferred_language": language,
        },
    )


# ==================================================
# 1. Combined Emergency
# ==================================================

def test_combined_emergency():

    with (
        patch(
            "main.assess_message",
            return_value=fake_safety(
                SafetyLevel.CRISIS
            ),
        ),
        patch(
            "main.assess_medical_safety",
            return_value=fake_medical(
                True,
                "chest_pain",
            ),
        ),
    ):

        response = post_chat(
            "I am in immediate danger and have chest pain."
        )

    assert response.status_code == 200

    text = response.json()["response"].lower()

    assert "emergency" in text
    assert "ambulance" in text
    assert "hurt yourself" in text
    assert "do not drive" in text


# ==================================================
# 2. Mental-Health Crisis Only
# ==================================================

def test_mental_crisis_only():

    with (
        patch(
            "main.assess_message",
            return_value=fake_safety(
                SafetyLevel.CRISIS
            ),
        ),
        patch(
            "main.assess_medical_safety",
            return_value=fake_medical(False),
        ),
    ):

        response = post_chat(
            "I am planning to hurt myself."
        )

    assert response.status_code == 200

    text = response.json()["response"].lower()

    assert "emergency" in text
    assert "hurt yourself" in text


# ==================================================
# 3. Medical Emergency Only
# ==================================================

def test_medical_emergency_only():

    with (
        patch(
            "main.assess_message",
            return_value=fake_safety(
                SafetyLevel.NORMAL
            ),
        ),
        patch(
            "main.assess_medical_safety",
            return_value=fake_medical(
                True,
                "breathing_difficulty",
            ),
        ),
    ):

        response = post_chat(
            "I cannot breathe properly."
        )

    assert response.status_code == 200

    text = response.json()["response"].lower()

    assert "medical emergency" in text
    assert "ambulance" in text


# ==================================================
# 4. AWS Failure + Medical Emergency
# ==================================================

def test_aws_failure_with_medical_emergency():

    with (
        patch(
            "main.assess_message",
            side_effect=RuntimeError(
                "AWS unavailable"
            ),
        ),
        patch(
            "main.assess_medical_safety",
            return_value=fake_medical(
                True,
                "chest_pain",
            ),
        ),
    ):

        response = post_chat(
            "I have severe chest pain."
        )

    assert response.status_code == 200

    text = response.json()["response"].lower()

    assert "ambulance" in text
    assert "emergency" in text


# ==================================================
# 5. Localized Medical Emergency Messages
# ==================================================

@pytest.mark.parametrize(
    "language, expected",
    [
        ("en", "emergency"),
        ("roman_ur", "ambulance"),
        ("ur", "ایمرجنسی"),
    ],
)
def test_localized_medical_emergency(
    language,
    expected,
):

    with (
        patch(
            "main.assess_message",
            return_value=fake_safety(
                SafetyLevel.NORMAL
            ),
        ),
        patch(
            "main.assess_medical_safety",
            return_value=fake_medical(
                True,
                "chest_pain",
            ),
        ),
    ):

        response = post_chat(
            "Medical emergency test",
            language,
        )

    assert response.status_code == 200

    assert expected in response.json()["response"]


# ==================================================
# 6. Localized Combined Emergency
# ==================================================

@pytest.mark.parametrize(
    "language",
    ["en", "roman_ur", "ur", "es", "de"],
)
def test_localized_combined_emergency(language):
    # Both emergencies are independently confirmed.
    with (
        patch(
            "main.assess_message",
            return_value=fake_safety(SafetyLevel.CRISIS),
        ),
        patch(
            "main.assess_medical_safety",
            return_value=fake_medical(True, "chest_pain"),
        ),
        patch(
            "main.assess_crisis_fallback",
            return_value=SimpleNamespace(explicit_crisis=True),
        ),
    ):
        response = post_chat(
            "Combined emergency test",
            language,
        )

    assert response.status_code == 200

    assert response.json()["response"] == (
        main.combined_emergency_text(
            "chest_pain",
            language,
        )
    )

    assert response.json()["session_id"]

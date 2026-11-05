
"""
MindBridge AI - Safety Failure Scenario Tests

Tests:
1. AWS unavailable, no medical emergency
2. AWS unavailable, medical emergency only
3. Medical Guardian unavailable, AWS crisis detected

All external AI services are mocked.
"""

from types import SimpleNamespace
from unittest.mock import patch

from fastapi.testclient import TestClient

import main
from safety_guardian import SafetyLevel


def fake_safety(level):
    return SimpleNamespace(
        level=level,
        reason="Test assessment",
        requires_professional_help=False,
    )


def fake_medical(emergency=False, category=None):
    return SimpleNamespace(
        emergency_detected=emergency,
        category=category,
        reason="Test assessment",
        uncertain=False,
    )


def post_chat(message):
    with TestClient(main.app) as client:
        return client.post(
            "/chat",
            json={
                "message": message,
                "language_mode": "manual",
                "preferred_language": "en",
            },
        )


def test_aws_failure_without_medical_emergency():

    with (
        patch(
            "main.assess_message",
            side_effect=RuntimeError("AWS unavailable"),
        ),
        patch(
            "main.assess_medical_safety",
            return_value=fake_medical(False),
        ),
    ):
        response = post_chat(
            "I feel emotionally overwhelmed."
        )

    assert response.status_code == 200

    assert response.json()["response"] == (
        main.safety_text("fallback", "en")
    )



def test_aws_failure_with_medical_only():

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
            "I have sudden severe chest pain."
        )

    assert response.status_code == 200

    text = response.json()["response"].lower()

    # Medical emergency guidance must be present.
    assert "ambulance" in text

    # Do not add unsupported self-harm assumptions.
    assert "hurt yourself" not in text



def test_medical_guardian_failure_with_mental_crisis():

    with (
        patch(
            "main.assess_medical_safety",
            side_effect=RuntimeError(
                "Medical Guardian unavailable"
            ),
        ),
        patch(
            "main.assess_message",
            return_value=fake_safety(
                SafetyLevel.CRISIS
            ),
        ),
    ):
        response = post_chat(
            "I am planning to hurt myself tonight."
        )

    assert response.status_code == 200

    text = response.json()["response"].lower()

    assert "emergency" in text
    assert "hurt yourself" in text

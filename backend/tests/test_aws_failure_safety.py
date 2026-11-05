
"""
MindBridge AI - AWS Failure Safety Test

Verifies current behavior when AWS safety
assessment is unavailable during a medical
emergency.

No real AWS or OpenAI calls.
"""

from types import SimpleNamespace
from unittest.mock import patch

from fastapi.testclient import TestClient

import main


def test_aws_failure_combined_risk():

    client = TestClient(main.app)

    with (
        patch(
            "main.assess_message",
            side_effect=RuntimeError(
                "AWS service unavailable"
            ),
        ),
        patch(
            "main.assess_medical_safety",
            return_value=SimpleNamespace(
                emergency_detected=True,
                category="chest_pain",
                reason="Test emergency",
                uncertain=False,
            ),
        ),
    ):

        response = client.post(
            "/chat",
            json={
                "message": (
                    "I am planning to end my life "
                    "tonight and I have a plan. "
                    "I also have severe chest pain."
                ),
                "language_mode": "manual",
                "preferred_language": "en",
            },
        )

    assert response.status_code == 200

    text = response.json()["response"].lower()

    assert "ambulance" in text

    # This assertion documents the safety gap.
    # It is expected to FAIL before the fix.
    assert "hurt yourself" in text

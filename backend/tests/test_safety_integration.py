
"""
MindBridge AI - Safety Integration Regression Tests

Run:
    python -m pytest tests/test_safety_integration.py -v

These tests verify deterministic safety behavior,
localized response availability and FastAPI routing.

External AWS/OpenAI calls are not required.
Passing tests do not constitute clinical certification.
"""

import pytest
from fastapi.testclient import TestClient

import main

from crisis_rules import detect_unsafe_location

from language_registry import is_language_enabled

from safety_responses import (
    SAFETY_MESSAGES,
    get_safety_response_by_language,
    validate_safety_localizations,
)


SUPPORTED_LANGUAGES = (
    "en",
    "roman_ur",
    "ur",
    "es",
    "de",
)

REQUIRED_SAFETY_TYPES = {
    "crisis",
    "crisis_ongoing",
    "clarification",
    "followup",
    "fallback",
    "escalation",
    "service_unavailable",
    "unsafe_location",
}


# ==================================================
# 1. LANGUAGE RESPONSE VALIDATION
# ==================================================

@pytest.mark.parametrize(
    "language",
    SUPPORTED_LANGUAGES,
)
def test_language_has_required_safety_messages(language):
    assert REQUIRED_SAFETY_TYPES.issubset(
        set(SAFETY_MESSAGES[language])
    )

    for response_type in REQUIRED_SAFETY_TYPES:
        text = SAFETY_MESSAGES[language][response_type]

        assert isinstance(text, str)
        assert text.strip()


def test_safety_localization_validation():
    validate_safety_localizations()


# ==================================================
# 2. LOCALIZED SAFETY RESPONSE RETRIEVAL
# ==================================================

@pytest.mark.parametrize(
    "language",
    SUPPORTED_LANGUAGES,
)
@pytest.mark.parametrize(
    "response_type",
    sorted(REQUIRED_SAFETY_TYPES),
)
def test_localized_safety_response(language, response_type):
    response = get_safety_response_by_language(
        response_type,
        language,
    )

    assert response == SAFETY_MESSAGES[language][response_type]
    assert response.strip()


# ==================================================
# 3. UNSAFE-LOCATION DETECTION
# ==================================================

@pytest.mark.parametrize(
    "message",
    [
        (
            "I'm standing near the edge of a rooftop "
            "and I don't feel safe."
        ),
        (
            "I am sitting at the edge of a balcony "
            "and I feel unsafe."
        ),
        (
            "I'm walking near the edge of a cliff."
        ),
    ],
)
def test_unsafe_location_positive(message):
    assert detect_unsafe_location(message) is True


@pytest.mark.parametrize(
    "message",
    [
        "I visited a rooftop restaurant yesterday.",
        "The rooftop has a beautiful view.",
        "I am not standing near the edge of a rooftop.",
        "I am feeling stressed about my work.",
        "I need help preparing for my exam.",
    ],
)
def test_unsafe_location_negative(message):
    assert detect_unsafe_location(message) is False


# ==================================================
# 4. API HEALTH
# ==================================================

def test_health_endpoint():
    with TestClient(main.app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_application_version():
    assert main.APP_VERSION == "1.6.7"


# ==================================================
# 5. FASTAPI EMERGENCY ROUTING
# ==================================================

def test_rooftop_emergency_route(monkeypatch):
    """
    Test the actual /chat route.

    Medical screening is replaced to make this
    specific test deterministic. The unsafe-location
    detector and chat routing remain real.
    """

    class MedicalResult:
        emergency_detected = False
        category = None

    monkeypatch.setattr(
        main,
        "assess_medical_safety",
        lambda message: MedicalResult(),
    )

    with TestClient(main.app) as client:
        response = client.post(
            "/chat",
            json={
                "message": (
                    "I'm standing near the edge "
                    "of a rooftop and I don't feel safe."
                )
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["session_id"]
    assert data["response"].strip()

    expected = SAFETY_MESSAGES["en"]["unsafe_location"]

    assert data["response"] == expected


# ==================================================
# 6. MEDICAL EMERGENCY RESPONSE
# ==================================================

@pytest.mark.parametrize(
    "language",
    SUPPORTED_LANGUAGES,
)
@pytest.mark.parametrize(
    "category",
    [
        "stroke_warning",
        "sudden_vision_loss",
        "severe_eye_pain",
    ],
)
def test_medical_emergency_messages(language, category):
    response = main.medical_emergency_text(
        category,
        language,
    )

    assert isinstance(response, str)
    assert response.strip()


# ==================================================
# 7. ENABLED LANGUAGE POLICY
# ==================================================

@pytest.mark.parametrize(
    "language",
    SUPPORTED_LANGUAGES,
)
def test_all_supported_languages_enabled(language):
    assert is_language_enabled(language) is True


@pytest.mark.parametrize(
    "language",
    ["ar", "hi", "unknown"],
)
def test_unsupported_languages_disabled(language):
    assert is_language_enabled(language) is False


# ==================================================
# 8. TEST COMPLETION
# ==================================================

if __name__ == "__main__":
    raise SystemExit(
        pytest.main([__file__, "-v"])
    )

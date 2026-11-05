
from fastapi.testclient import TestClient

import main
from conversation_store import conversation_store
from safety_guardian import SafetyLevel, SafetyResult


def fake_safe_assessment(message):
    return SafetyResult(
        level=SafetyLevel.NORMAL,
        requires_professional_help=False,
        reason="No immediate concern detected",
    )


def fake_agent():
    class Agent:
        def __call__(self, prompt):
            return "I am here to support you."

    return Agent()


def fake_validator(message, response):
    return {
        "approved": True,
        "issues": [],
        "requires_human_review": False,
    }


def test_new_chat_creates_secure_cookie(monkeypatch):
    monkeypatch.setattr(
        main, "assess_message", fake_safe_assessment
    )
    monkeypatch.setattr(
        main, "create_agent", fake_agent
    )
    monkeypatch.setattr(
        main, "validate_response", fake_validator
    )

    with TestClient(main.app) as client:
        response = client.post(
            "/chat",
            json={"message": "Hello"},
        )

        assert response.status_code == 200

        assert response.json()["session_id"]

        assert "mindbridge_session" in client.cookies

        cookie_header = response.headers.get(
            "set-cookie", ""
        ).lower()

        assert "httponly" in cookie_header
        assert "samesite=strict" in cookie_header

        if main.IS_PRODUCTION:
            assert "secure" in cookie_header


def test_valid_cookie_allows_existing_session(monkeypatch):
    monkeypatch.setattr(
        main, "assess_message", fake_safe_assessment
    )
    monkeypatch.setattr(
        main, "create_agent", fake_agent
    )
    monkeypatch.setattr(
        main, "validate_response", fake_validator
    )

    session, token = (
        conversation_store.create_secure_session()
    )

    with TestClient(main.app) as client:
        client.cookies.set(
            "mindbridge_session",
            token,
        )

        response = client.post(
            "/chat",
            json={
                "message": "I feel stressed today.",
                "session_id": session.session_id,
            },
        )

        assert response.status_code == 200

        assert (
            response.json()["session_id"]
            == session.session_id
        )


def test_trusted_origin_allows_chat(monkeypatch):
    monkeypatch.setattr(
        main, "assess_message", fake_safe_assessment
    )
    monkeypatch.setattr(
        main, "create_agent", fake_agent
    )
    monkeypatch.setattr(
        main, "validate_response", fake_validator
    )

    with TestClient(main.app) as client:
        response = client.post(
            "/chat",
            headers={
                "Origin": main.ALLOWED_ORIGINS[0],
            },
            json={
                "message": "Hello MindBridge",
            },
        )

        assert response.status_code == 200

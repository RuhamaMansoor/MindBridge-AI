
import pytest
from fastapi.testclient import TestClient

import main


@pytest.fixture
def client():
    return TestClient(main.app)


def test_chat_rejects_empty_message(client):
    response = client.post(
        "/chat",
        json={"message": ""}
    )

    assert response.status_code == 422


def test_chat_rejects_message_over_limit(client):
    response = client.post(
        "/chat",
        json={"message": "a" * 2001}
    )

    assert response.status_code == 422


def test_chat_rejects_invalid_language(client):
    response = client.post(
        "/chat",
        json={
            "message": "Hello",
            "language_mode": "manual",
            "preferred_language": "invalid"
        }
    )

    assert response.status_code == 422


def test_chat_accepts_valid_request_schema(client, monkeypatch):
    # Simulate a safety assessment failure.
    # The application should use its safe fallback,
    # without calling any external AI provider.

    def fake_assess_message(message):
        raise RuntimeError("Simulated safety service failure")

    monkeypatch.setattr(
        main,
        "assess_message",
        fake_assess_message
    )

    response = client.post(
        "/chat",
        json={
            "message": "I feel stressed today.",
            "language_mode": "manual",
            "preferred_language": "en"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data["response"], str)
    assert len(data["response"]) > 0
    assert isinstance(data["session_id"], str)
    assert len(data["session_id"]) > 0


def test_crisis_bypasses_normal_ai(client, monkeypatch):
    from safety_guardian import SafetyLevel, SafetyResult

    def fake_assess_message(message):
        return SafetyResult(
            level=SafetyLevel.CRISIS,
            requires_professional_help=True,
            reason="Simulated crisis for automated testing",
        )

    def forbidden_create_agent():
        raise AssertionError(
            "Normal AI agent must not run during crisis"
        )

    monkeypatch.setattr(
        main, "assess_message", fake_assess_message
    )
    monkeypatch.setattr(
        main, "create_agent", forbidden_create_agent
    )

    response = client.post(
        "/chat",
        json={
            "message": "Simulated safety test message",
            "language_mode": "manual",
            "preferred_language": "en",
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data["response"], str)
    assert data["response"].strip()
    assert data["session_id"]


def test_uncertain_safety_requires_clarification(client, monkeypatch):
    from safety_guardian import SafetyLevel, SafetyResult
    from conversation_store import conversation_store

    def fake_assess_message(message):
        return SafetyResult(
            level=SafetyLevel.REVIEW,
            requires_professional_help=True,
            reason="Safety concern requires clarification",
        )

    def forbidden_create_agent():
        raise AssertionError(
            "Normal AI must not run while clarification is pending"
        )

    monkeypatch.setattr(
        main, "assess_message", fake_assess_message
    )
    monkeypatch.setattr(
        main, "create_agent", forbidden_create_agent
    )

    response = client.post(
        "/chat",
        json={
            "message": "Simulated ambiguous safety message",
            "language_mode": "manual",
            "preferred_language": "en",
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["response"].strip()

    state = conversation_store.get_safety_state(
        data["session_id"]
    )

    assert state["pending_safety_check"] is True
    assert state["safety_followup_count"] == 0
    assert state["safety_status"] == "pending"


def test_unresolved_safety_escalates_after_three_followups(
    client, monkeypatch
):
    from safety_guardian import SafetyLevel, SafetyResult
    from conversation_store import conversation_store
    from types import SimpleNamespace

    def fake_assess_message(message):
        return SafetyResult(
            level=SafetyLevel.REVIEW,
            requires_professional_help=True,
            reason="Safety concern requires clarification",
        )

    def fake_assess_followup(message, history):
        return SimpleNamespace(
            safety=SafetyResult(
                level=SafetyLevel.REVIEW,
                requires_professional_help=True,
                reason="Safety concern requires clarification",
            ),
            resolution_evidence=False,
        )

    def forbidden_create_agent():
        raise AssertionError(
            "Normal AI must not run during unresolved safety escalation"
        )

    monkeypatch.setattr(
        main, "assess_message", fake_assess_message
    )
    monkeypatch.setattr(
        main, "assess_followup_detailed", fake_assess_followup
    )
    monkeypatch.setattr(
        main, "create_agent", forbidden_create_agent
    )

    payload = {
        "message": "Simulated ambiguous safety message",
        "language_mode": "manual",
        "preferred_language": "en",
    }

    first_response = client.post("/chat", json=payload)

    assert first_response.status_code == 200

    sid = first_response.json()["session_id"]

    for number in range(1, 4):
        response = client.post(
            "/chat",
            json={
                **payload,
                "message": "I am still unsure.",
                "session_id": sid,
            },
        )

        assert response.status_code == 200
        assert response.json()["response"].strip()

        state = conversation_store.get_safety_state(sid)

        assert state["safety_followup_count"] == number

    assert state["pending_safety_check"] is True
    assert state["safety_status"] == "escalated"


def test_safety_resolution_resets_escalation(
    client, monkeypatch
):
    from safety_guardian import SafetyLevel, SafetyResult
    from conversation_store import conversation_store

    session, token = conversation_store.create_secure_session()
    sid = session.session_id

    client.cookies.set(
        "mindbridge_session",
        token,
    )


    conversation_store.set_pending_safety(sid, True)

    for _ in range(3):
        conversation_store.increment_safety_followup(sid)

    before = conversation_store.get_safety_state(sid)

    assert before["safety_status"] == "escalated"
    assert before["safety_followup_count"] == 3

    def fake_followup(message, history):
        from types import SimpleNamespace

        return SimpleNamespace(
            safety=SafetyResult(
                level=SafetyLevel.NORMAL,
                requires_professional_help=False,
                reason="No immediate concern detected",
            ),
            resolution_evidence=True,
        )

    class FakeAgent:
        def __call__(self, message):
            from types import SimpleNamespace

            return SimpleNamespace(
                message={
                    "content": [
                        {
                            "text": (
                                "Thank you for clarifying. "
                                "Let's discuss ways to manage stress."
                            )
                        }
                    ]
                }
            )

    def fake_validator(message, response, conversation_history=None):
        return {
            "approved": True,
            "issues": [],
            "requires_human_review": False,
        }

    monkeypatch.setattr(
        main, "assess_followup_detailed", fake_followup
    )
    monkeypatch.setattr(
        main, "create_agent", lambda: FakeAgent()
    )
    monkeypatch.setattr(
        main, "validate_response", fake_validator
    )

    response = client.post(
        "/chat",
        json={
            "message": (
                "I have no intention of harming myself, "
                "I have no plan, and I am with a trusted "
                "family member who is supporting me."
            ),
            "session_id": sid,
            "language_mode": "manual",
            "preferred_language": "en",
        },
    )

    assert response.status_code == 200
    assert response.json()["response"].strip()

    after = conversation_store.get_safety_state(sid)

    assert after["pending_safety_check"] is False
    assert after["safety_followup_count"] == 0
    assert after["safety_status"] == "normal"

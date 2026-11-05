
from fastapi.testclient import TestClient

import main
from conversation_store import conversation_store


def test_missing_session_cookie_rejected():
    session, token = (
        conversation_store.create_secure_session()
    )

    with TestClient(main.app) as client:
        response = client.post(
            "/chat",
            json={
                "message": "Hello",
                "session_id": session.session_id,
            },
        )

    assert response.status_code == 403


def test_invalid_session_cookie_rejected():
    session, token = (
        conversation_store.create_secure_session()
    )

    with TestClient(main.app) as client:
        client.cookies.set(
            "mindbridge_session",
            "invalid-token",
        )

        response = client.post(
            "/chat",
            json={
                "message": "Hello",
                "session_id": session.session_id,
            },
        )

    assert response.status_code == 403


def test_other_session_cookie_rejected():
    first_session, first_token = (
        conversation_store.create_secure_session()
    )

    second_session, second_token = (
        conversation_store.create_secure_session()
    )

    with TestClient(main.app) as client:
        client.cookies.set(
            "mindbridge_session",
            second_token,
        )

        response = client.post(
            "/chat",
            json={
                "message": "Hello",
                "session_id": first_session.session_id,
            },
        )

    assert response.status_code == 403


def test_untrusted_origin_rejected():
    with TestClient(main.app) as client:
        response = client.post(
            "/chat",
            headers={
                "Origin": "https://untrusted.example",
            },
            json={
                "message": "Hello",
            },
        )

    assert response.status_code == 403


def test_cross_site_request_rejected():
    with TestClient(main.app) as client:
        response = client.post(
            "/chat",
            headers={
                "Sec-Fetch-Site": "cross-site",
            },
            json={
                "message": "Hello",
            },
        )

    assert response.status_code == 403

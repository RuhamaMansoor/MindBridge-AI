
from conversation_store import ConversationStore


def test_secure_session_creation():
    store = ConversationStore()

    session, token = store.create_secure_session()

    assert session.session_id
    assert isinstance(token, str)
    assert len(token) >= 40
    assert session.token_hash is not None
    assert session.token_hash != token


def test_valid_owner_token():
    store = ConversationStore()

    session, token = store.create_secure_session()

    assert store.verify_session_ownership(
        session.session_id,
        token,
    ) is True


def test_invalid_owner_token():
    store = ConversationStore()

    session, token = store.create_secure_session()

    assert store.verify_session_ownership(
        session.session_id,
        "incorrect-token",
    ) is False


def test_other_session_token_is_rejected():
    store = ConversationStore()

    first_session, first_token = (
        store.create_secure_session()
    )

    second_session, second_token = (
        store.create_secure_session()
    )

    assert store.verify_session_ownership(
        first_session.session_id,
        second_token,
    ) is False

    assert store.verify_session_ownership(
        second_session.session_id,
        first_token,
    ) is False


def test_missing_session_is_rejected():
    store = ConversationStore()

    assert store.verify_session_ownership(
        "non-existent-session",
        "any-token",
    ) is False


def test_legacy_session_has_no_owner_token():
    store = ConversationStore()

    session = store.create_session()

    assert store.verify_session_ownership(
        session.session_id,
        "any-token",
    ) is False


from session_security import (
    generate_session_token,
    hash_session_token,
    verify_session_token,
)


def test_token_is_unique():
    first = generate_session_token()
    second = generate_session_token()

    assert first != second


def test_token_has_sufficient_length():
    token = generate_session_token()

    assert len(token) >= 40


def test_correct_token_is_accepted():
    token = generate_session_token()
    stored_hash = hash_session_token(token)

    assert verify_session_token(token, stored_hash) is True


def test_wrong_token_is_rejected():
    token = generate_session_token()
    stored_hash = hash_session_token(token)

    assert verify_session_token(
        "incorrect-token",
        stored_hash,
    ) is False


def test_empty_token_is_rejected():
    token = generate_session_token()
    stored_hash = hash_session_token(token)

    assert verify_session_token("", stored_hash) is False


def test_raw_token_is_not_stored_as_hash():
    token = generate_session_token()
    stored_hash = hash_session_token(token)

    assert token != stored_hash
    assert len(stored_hash) == 64

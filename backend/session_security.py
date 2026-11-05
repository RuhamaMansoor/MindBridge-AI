
import hashlib
import hmac
import secrets


TOKEN_BYTES = 32


def generate_session_token() -> str:
    """
    Generate a cryptographically secure
    random session token.
    """
    return secrets.token_urlsafe(TOKEN_BYTES)


def hash_session_token(token: str) -> str:
    """
    Hash the token before storing it.
    Never store raw session tokens.
    """
    if not isinstance(token, str) or not token:
        raise ValueError("Invalid session token")

    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()


def verify_session_token(
    supplied_token: str,
    stored_token_hash: str,
) -> bool:
    """
    Verify a supplied token using
    constant-time hash comparison.
    """
    if (
        not isinstance(supplied_token, str)
        or not supplied_token
        or not isinstance(stored_token_hash, str)
        or not stored_token_hash
    ):
        return False

    supplied_hash = hash_session_token(
        supplied_token
    )

    return hmac.compare_digest(
        supplied_hash,
        stored_token_hash,
    )

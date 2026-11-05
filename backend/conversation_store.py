
from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import RLock
from uuid import uuid4

from session_security import (
    generate_session_token,
    hash_session_token,
    verify_session_token,
)


MAX_MESSAGES = 20
MAX_SESSIONS = 100
SESSION_TTL_SECONDS = 1800
MAX_SAFETY_FOLLOWUPS = 3


@dataclass
class ConversationSession:
    session_id: str

    messages: list[dict] = field(default_factory=list)

    pending_safety_check: bool = False
    safety_concern_type: str = "none"
    safety_followup_count: int = 0
    safety_status: str = "normal"

    language_mode: str = "auto"
    preferred_language: str | None = None

    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    # Store only the hash, never the raw token.
    token_hash: str | None = field(
        default=None,
        repr=False,
    )


class ConversationStore:

    def __init__(self):
        self._sessions = {}
        self._lock = RLock()

    def _now(self):
        return datetime.now(timezone.utc)

    def _cleanup(self):
        now = self._now()

        expired = [
            session_id
            for session_id, session in self._sessions.items()
            if (
                now - session.updated_at
            ).total_seconds() > SESSION_TTL_SECONDS
        ]

        for session_id in expired:
            del self._sessions[session_id]

    def create_session(self):
        with self._lock:
            self._cleanup()

            if len(self._sessions) >= MAX_SESSIONS:
                oldest_id = min(
                    self._sessions,
                    key=lambda sid:
                    self._sessions[sid].updated_at
                )
                del self._sessions[oldest_id]

            session_id = str(uuid4())

            session = ConversationSession(
                session_id=session_id
            )

            self._sessions[session_id] = session

            return session

    def create_secure_session(self):
        """
        Create a session with a secret ownership token.

        Return the raw token only once to the caller.
        The store retains only its hash.
        """
        with self._lock:
            session = self.create_session()
            token = generate_session_token()

            session.token_hash = hash_session_token(
                token
            )

            return session, token

    def verify_session_ownership(
        self,
        session_id,
        token,
    ):
        """
        Verify ownership without exposing the stored hash.
        """
        with self._lock:
            self._cleanup()

            session = self._sessions.get(session_id)

            if not session or not session.token_hash:
                return False

            return verify_session_token(
                token,
                session.token_hash,
            )

    def get_session(self, session_id):
        with self._lock:
            self._cleanup()

            session = self._sessions.get(session_id)

            if session:
                session.updated_at = self._now()

            return session

    def get_conversation_history(
        self,
        session_id: str,
        limit: int = 10,
    ) -> list[dict]:
        """
        Return a safe copy of recent conversation messages.

        The caller must verify session ownership
        before requesting history.
        """

        with self._lock:
            session = self.get_session(session_id)

            if session is None:
                return []

            limit = max(1, min(int(limit), MAX_MESSAGES))

            return [
                {
                    "role": message["role"],
                    "content": message["content"],
                }
                for message in session.messages[-limit:]
                if (
                    isinstance(message, dict)
                    and message.get("role")
                    in {"user", "assistant"}
                    and isinstance(
                        message.get("content"),
                        str,
                    )
                )
            ]


    def add_message(
        self,
        session_id,
        role,
        content,
    ):
        with self._lock:
            session = self.get_session(session_id)

            if not session:
                return False

            session.messages.append({
                "role": role,
                "content": content,
            })

            session.messages = session.messages[
                -MAX_MESSAGES:
            ]

            session.updated_at = self._now()

            return True

    
    def set_pending_safety(
        self,
        session_id,
        pending,
    ):
        with self._lock:
            session = self.get_session(session_id)

            if session is None:
                return False

            session.pending_safety_check = bool(pending)

            if not pending:
                session.safety_concern_type = "none"
                session.safety_followup_count = 0
                session.safety_status = "normal"

            else:
                if session.safety_concern_type not in {
                    "clarification",
                    "crisis",
                }:
                    session.safety_concern_type = (
                        "clarification"
                    )

                if session.safety_status not in {
                    "pending",
                    "escalated",
                }:
                    session.safety_status = "pending"

            session.updated_at = self._now()
            return True

    def increment_safety_followup(
        self,
        session_id,
    ):
        with self._lock:
            session = self.get_session(session_id)

            if not session:
                return None

            session.safety_followup_count += 1

            if (
                session.safety_followup_count
                >= MAX_SAFETY_FOLLOWUPS
            ):
                session.safety_status = "escalated"
            else:
                session.safety_status = "pending"

            session.updated_at = self._now()

            return session.safety_followup_count

    def get_safety_state(
    self,
    session_id,
):
        with self._lock:
            session = self.get_session(session_id)

        if not session:
            return None

        return {
            "pending_safety_check":
                session.pending_safety_check,
            "safety_concern_type":
                session.safety_concern_type,
            "safety_followup_count":
                session.safety_followup_count,
            "safety_status":
                session.safety_status,
        }


    def set_safety_concern(
        self,
        session_id: str,
        concern_type: str,
    ) -> bool:
        """
        Track the reason for a pending safety concern.
        Technical failures must not be treated as
        confirmed self-harm concerns.
        """

        allowed_types = {
            "none",
            "clarification",
            "crisis",
            "assessment_unavailable",
        }

        if concern_type not in allowed_types:
            raise ValueError(
                "Invalid safety concern type"
            )

        with self._lock:
            session = self.get_session(session_id)

            if session is None:
                return False

            session.safety_concern_type = concern_type

            if concern_type == "none":
                session.pending_safety_check = False
                session.safety_followup_count = 0
                session.safety_status = "normal"

            elif concern_type == "assessment_unavailable":
                session.pending_safety_check = False
                session.safety_followup_count = 0
                session.safety_status = (
                    "assessment_unavailable"
                )

            else:
                session.pending_safety_check = True
                session.safety_followup_count = 0
                session.safety_status = "pending"

            session.updated_at = self._now()

            return True



conversation_store = ConversationStore()

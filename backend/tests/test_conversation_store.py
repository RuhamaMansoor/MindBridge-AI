
from conversation_store import conversation_store


def test_session_creation():
    session = conversation_store.create_session()

    assert session.session_id
    assert session.pending_safety_check is False

    retrieved = conversation_store.get_session(
        session.session_id
    )

    assert retrieved is not None
    assert retrieved.session_id == session.session_id


def test_safety_pending_state():
    session = conversation_store.create_session()
    sid = session.session_id

    conversation_store.set_pending_safety(sid, True)

    state = conversation_store.get_safety_state(sid)

    assert state["pending_safety_check"] is True
    assert state["safety_followup_count"] == 0
    assert state["safety_status"] == "pending"


def test_safety_followup_counter():
    session = conversation_store.create_session()
    sid = session.session_id

    conversation_store.set_pending_safety(sid, True)

    conversation_store.increment_safety_followup(sid)

    state = conversation_store.get_safety_state(sid)

    assert state["safety_followup_count"] == 1
    assert state["safety_status"] == "pending"


def test_escalation_after_three_followups():
    session = conversation_store.create_session()
    sid = session.session_id

    conversation_store.set_pending_safety(sid, True)

    for _ in range(3):
        conversation_store.increment_safety_followup(sid)

    state = conversation_store.get_safety_state(sid)

    assert state["pending_safety_check"] is True
    assert state["safety_followup_count"] == 3
    assert state["safety_status"] == "escalated"


def test_safety_resolution_resets_counter():
    session = conversation_store.create_session()
    sid = session.session_id

    conversation_store.set_pending_safety(sid, True)

    for _ in range(3):
        conversation_store.increment_safety_followup(sid)

    conversation_store.set_pending_safety(sid, False)

    state = conversation_store.get_safety_state(sid)

    assert state["pending_safety_check"] is False
    assert state["safety_followup_count"] == 0
    assert state["safety_status"] == "normal"


def test_sessions_are_independent():
    first = conversation_store.create_session()
    second = conversation_store.create_session()

    conversation_store.set_pending_safety(
        first.session_id,
        True,
    )

    conversation_store.increment_safety_followup(
        first.session_id
    )

    first_state = conversation_store.get_safety_state(
        first.session_id
    )

    second_state = conversation_store.get_safety_state(
        second.session_id
    )

    assert first_state["safety_followup_count"] == 1
    assert second_state["safety_followup_count"] == 0
    assert second_state["pending_safety_check"] is False

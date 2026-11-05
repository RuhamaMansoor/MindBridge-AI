
"""
MindBridge AI - Crisis Fallback Tests

Tests explicit crisis detection in English,
Roman Urdu and Urdu, plus basic negative cases.
"""

import pytest

from crisis_fallback import assess_crisis_fallback


@pytest.mark.parametrize(
    "message",
    [
        "I am planning to kill myself tonight",
        "I want to die",
        "I am going to end my life",
        "Main khudkushi karna chahti hoon",
        "Main apni jaan lena chahta hoon",
        "میں خودکشی کرنا چاہتی ہوں",
        "میں مرنا چاہتا ہوں",
    ],
)
def test_explicit_crisis_detected(message):

    result = assess_crisis_fallback(message)

    assert result.explicit_crisis is True
    assert result.uncertain is True


@pytest.mark.parametrize(
    "message",
    [
        "I feel stressed today",
        "I have a headache",
        "I need someone to talk to",
        "Main aaj udaas hoon",
        "آج میں پریشان ہوں",
        "",
    ],
)
def test_non_explicit_messages(message):

    result = assess_crisis_fallback(message)

    assert result.explicit_crisis is False
    assert result.uncertain is True


def test_invalid_input():

    result = assess_crisis_fallback(None)

    assert result.explicit_crisis is False
    assert result.uncertain is True

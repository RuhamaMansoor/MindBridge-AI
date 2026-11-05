
"""
MindBridge AI - Language Detector Tests

Tests language detection, registry configuration,
enabled language instructions, and fallback behavior.

Spanish and German are enabled in the registry.
Automatic detection requires separate verification.
"""

import pytest

from language_detector import detect_language

from language_registry import (
    LANGUAGES,
    get_enabled_languages,
    get_language_instruction,
    is_language_enabled,
    list_languages,
)


SUPPORTED_LANGUAGES = {
    "en",
    "ur",
    "roman_ur",
    "es",
    "de",
}


# ==================================================
# 1. EXISTING LANGUAGE DETECTION
# ==================================================

@pytest.mark.parametrize(
    "message, expected",
    [
        ("I feel stressed today", "en"),
        ("I need someone to talk to", "en"),
        ("Mujhe aaj stress ho raha hai", "roman_ur"),
        ("Meri neend theek nahi hai", "roman_ur"),
        (
            "Kya aap meri madad kar sakte hain?",
            "roman_ur",
        ),
        ("مجھے آج پریشانی ہو رہی ہے", "ur"),
        ("آپ کیسے ہیں؟", "ur"),
    ],
)
def test_enabled_language_detection(message, expected):
    assert detect_language(message) == expected


# ==================================================
# 2. UNSUPPORTED LANGUAGE FALLBACK
# ==================================================

@pytest.mark.parametrize(
    "message",
    [
        "أشعر بالتوتر اليوم",
        "मुझे तनाव हो रहा है",
        "আমি আজ চিন্তিত",
        "今日は不安です",
        "오늘 불안해요",
    ],
)
def test_unsupported_languages_fallback_to_english(message):
    assert detect_language(message) == "en"


# ==================================================
# 3. INVALID AND EMPTY INPUT
# ==================================================

@pytest.mark.parametrize(
    "message",
    [
        "",
        "   ",
        None,
        123,
        [],
    ],
)
def test_invalid_or_empty_input(message):
    assert detect_language(message) == "en"


# ==================================================
# 4. ENABLED LANGUAGES
# ==================================================

def test_enabled_languages():
    assert set(get_enabled_languages()) == SUPPORTED_LANGUAGES


# ==================================================
# 5. TOTAL CONFIGURED LANGUAGES
# ==================================================

def test_total_languages():
    assert len(LANGUAGES) == 5
    assert set(LANGUAGES) == SUPPORTED_LANGUAGES


# ==================================================
# 6. LANGUAGE ENABLED STATUS
# ==================================================

@pytest.mark.parametrize(
    "language",
    ["en", "ur", "roman_ur", "es", "de"],
)
def test_supported_language_enabled(language):
    assert is_language_enabled(language) is True


@pytest.mark.parametrize(
    "language",
    ["ar", "hi", "unknown"],
)
def test_unsupported_language_disabled(language):
    assert is_language_enabled(language) is False


# ==================================================
# 7. ENABLED LANGUAGE INSTRUCTIONS
# ==================================================

@pytest.mark.parametrize(
    "language, expected_text",
    [
        ("en", "English"),
        ("ur", "Urdu"),
        ("roman_ur", "Roman Urdu"),
        ("es", "Spanish"),
        ("de", "German"),
    ],
)
def test_language_instructions(language, expected_text):
    instruction = get_language_instruction(language)

    assert isinstance(instruction, str)
    assert expected_text in instruction
    assert instruction == LANGUAGES[language].instruction


# ==================================================
# 8. UNSUPPORTED LANGUAGE INSTRUCTION FALLBACK
# ==================================================

@pytest.mark.parametrize(
    "language",
    ["ar", "hi", "unknown"],
)
def test_unsupported_language_instruction_fallback(language):
    english_instruction = LANGUAGES["en"].instruction

    assert (
        get_language_instruction(language)
        == english_instruction
    )


# ==================================================
# 9. UNSUPPORTED FALLBACK LANGUAGE
# ==================================================

def test_unsupported_fallback_reverts_to_english():
    assert detect_language(
        "I feel stressed",
        fallback="ar",
    ) == "en"


# ==================================================
# 10. LANGUAGE REGISTRY LIST
# ==================================================

def test_language_registry_list():
    languages = list_languages()

    assert len(languages) == 5

    assert {
        language["code"]
        for language in languages
    } == SUPPORTED_LANGUAGES

    for language in languages:
        assert isinstance(language["enabled"], bool)
        assert language["enabled"] is True
        assert language["name"]
        assert language["native_name"]


# ==================================================
# 11. KNOWN URDU DETECTION BEHAVIOR
# ==================================================

def test_known_urdu_detection_limitation():
    assert detect_language("سلام") == "ur"


# ==================================================
# 12. ALL FIVE LANGUAGES ENABLED
# ==================================================

def test_all_five_languages_enabled():
    for language in SUPPORTED_LANGUAGES:
        assert LANGUAGES[language].enabled is True


# ==================================================
# 13. LANGUAGE REGISTRY CONSISTENCY
# ==================================================

def test_language_registry_consistency():
    for code, language in LANGUAGES.items():
        assert language.code == code
        assert isinstance(language.instruction, str)
        assert language.instruction.strip()


if __name__ == "__main__":
    raise SystemExit(
        pytest.main([__file__, "-v"])
    )

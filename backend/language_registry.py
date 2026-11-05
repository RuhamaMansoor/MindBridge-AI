
"""
MindBridge AI - Language Registry

Central language configuration for MindBridge AI.

Supported languages:
1. English
2. Urdu
3. Roman Urdu
4. Spanish
5. German

Important:
Language availability does not establish clinical
or emergency-safety readiness. Multilingual crisis
detection, medical emergency screening, response
validation and localized messages require
independent testing before production release.
"""

from dataclasses import dataclass


# ==================================================
# 1. LANGUAGE MODEL
# ==================================================

@dataclass(frozen=True)
class Language:
    code: str
    name: str
    native_name: str
    instruction: str
    enabled: bool = False


# ==================================================
# 2. LANGUAGE REGISTRY
# ==================================================

LANGUAGES: dict[str, Language] = {

    # English
    "en": Language(
        code="en",
        name="English",
        native_name="English",
        instruction=(
            "Respond in clear, natural English. "
            "Use a warm, respectful and professional tone. "
            "Give practical and relevant answers. "
            "Avoid repetitive generic advice. "
            "Use clear explanations and actionable steps "
            "when appropriate."
        ),
        enabled=True,
    ),

    # Urdu
    "ur": Language(
        code="ur",
        name="Urdu",
        native_name="اردو",
        instruction=(
            "Respond in fluent, natural Urdu using "
            "Urdu script. "
            "Use respectful, compassionate and "
            "professional language. "
            "Explain ideas clearly and naturally. "
            "Provide practical guidance rather than "
            "unnecessary generic suggestions. "
            "Do not switch to Roman Urdu unless "
            "the user explicitly requests it."
        ),
        enabled=True,
    ),

    # Roman Urdu
    "roman_ur": Language(
        code="roman_ur",
        name="Roman Urdu",
        native_name="Roman Urdu",
        instruction=(
            "Respond in natural conversational Roman Urdu "
            "using Latin letters. "
            "Use familiar, respectful and easy-to-understand "
            "Pakistani Roman Urdu expressions. "
            "Avoid unnecessarily formal or robotic language. "
            "Give practical explanations and relevant steps. "
            "Do not use Urdu script unless the user "
            "explicitly requests it."
        ),
        enabled=True,
    ),

    # Spanish
    "es": Language(
        code="es",
        name="Spanish",
        native_name="Español",
        instruction=(
            "Respond in fluent, natural Spanish. "
            "Use respectful, empathetic and professional "
            "language. "
            "Provide clear, practical and context-aware "
            "guidance. "
            "Avoid repetitive generic advice. "
            "Do not switch languages unless requested. "
            "Use appropriate non-clinical mental "
            "wellness terminology."
        ),
        enabled=True,
    ),

    # German
    "de": Language(
        code="de",
        name="German",
        native_name="Deutsch",
        instruction=(
            "Respond in fluent, natural German. "
            "Use respectful, empathetic and professional "
            "language. "
            "Provide clear and actionable guidance. "
            "Avoid unnecessarily complicated explanations "
            "and repetitive generic suggestions. "
            "Do not switch languages unless requested. "
            "Use appropriate non-clinical mental "
            "wellness terminology."
        ),
        enabled=True,
    ),
}


# ==================================================
# 3. DEFAULT LANGUAGE
# ==================================================

DEFAULT_LANGUAGE = "en"


# ==================================================
# 4. GET ENABLED LANGUAGES
# ==================================================

def get_enabled_languages() -> dict[str, Language]:
    """
    Return all currently enabled languages.
    """

    return {
        code: language
        for code, language in LANGUAGES.items()
        if language.enabled
    }


# ==================================================
# 5. CHECK LANGUAGE AVAILABILITY
# ==================================================

def is_language_enabled(code: str) -> bool:
    """
    Check whether a language code is enabled.
    """

    if not isinstance(code, str):
        return False

    language = LANGUAGES.get(code)

    return bool(
        language is not None
        and language.enabled
    )


# ==================================================
# 6. GET LANGUAGE INSTRUCTIONS
# ==================================================

def get_language_instruction(code: str) -> str:
    """
    Return AI response instructions for a language.

    Unknown or disabled languages fall back
    to English.
    """

    language = LANGUAGES.get(code)

    if language is None or not language.enabled:
        language = LANGUAGES[DEFAULT_LANGUAGE]

    return language.instruction


# ==================================================
# 7. LIST ALL LANGUAGES
# ==================================================

def list_languages() -> list[dict]:
    """
    Return language information for frontend
    language selectors and API responses.
    """

    return [
        {
            "code": language.code,
            "name": language.name,
            "native_name": language.native_name,
            "enabled": language.enabled,
        }
        for language in LANGUAGES.values()
    ]

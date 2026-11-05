
"""
MindBridge AI - Deterministic Crisis Rules

These patterns are a safety layer, not a complete
clinical or multilingual risk assessment.
"""

import re
import unicodedata


CRISIS_PATTERNS = [
    # English
    r"\b(?:i want to|i am going to|i plan to|i intend to)\s+(?:kill myself|end my life|take my own life)\b",
    r"\b(?:i am|i'm)\s+(?:about to|ready to)\s+(?:kill myself|end my life)\b",

    # Roman Urdu
    r"\b(?:main|mein|mai)\s+(?:apni jaan khatam karna chahta|apni jaan khatam karna chahti|khudkushi karna chahta|khudkushi karna chahti)\b",
    r"\b(?:main|mein|mai)\s+(?:apni jaan khatam karne|khudkushi karne)\s+(?:ka|ki)\s+soch\s+(?:raha|rahi)\b",

    # Urdu
    r"(?:میں|ميں)\s+(?:خودکشی کرنا چاہتا|خودکشی کرنا چاہتی|اپنی جان ختم کرنا چاہتا|اپنی جان ختم کرنا چاہتی)",

    # Spanish
    r"\bquiero\s+(?:suicidarme|matarme|quitarme la vida)\b",
    r"\bvoy a\s+(?:suicidarme|matarme|quitarme la vida)\b",
    r"\bquiero\s+acabar\s+con\s+mi\s+vida\b",

    # German
    r"\bich\s+(?:will|möchte)\s+(?:mich töten|mein leben beenden|selbstmord begehen)\b",
    r"\bich\s+werde\s+(?:mich töten|mein leben beenden)\b",
]


UNSAFE_LOCATION_PATTERNS = [
    # English
    r"\b(?:i am|i'm)\s+(?:standing|sitting|walking)\s+(?:near|at|on)\s+(?:the\s+)?edge\s+of\s+(?:a\s+|the\s+)?(?:roof|rooftop|balcony|cliff)\b",

    r"\b(?:i am|i'm)\s+(?:on|at)\s+(?:a\s+|the\s+)?(?:roof|rooftop|balcony)\b.{0,100}\b(?:not safe|unsafe|might jump|want to jump)\b",

    # Spanish
    r"\b(?:estoy|me encuentro)\s+(?:al|en el|cerca del)\s+borde\s+de\s+(?:una?\s+)?(?:azotea|tejado|balcón|precipicio)\b",

    r"\bestoy\s+en\s+(?:una?\s+)?(?:azotea|tejado|balcón)\b.{0,100}\b(?:no me siento segur[oa]|quiero saltar|voy a saltar)\b",

    # German
    r"\bich\s+(?:stehe|sitze|bin)\s+(?:am|an dem)\s+rand\s+(?:eines?|des|der)\s+(?:daches|dachs|balkons|abgrunds)\b",

    r"\bich\s+bin\s+(?:auf dem|auf einem)\s+(?:dach|balkon)\b.{0,100}\b(?:nicht sicher|springen|hinunterspringen)\b",
]


NEGATED_UNSAFE_LOCATION_PATTERNS = [
    r"\b(?:i am not|i'm not)\s+(?:standing|sitting|walking)\s+(?:near|at|on)\s+(?:the\s+)?edge\b",
    r"\bno\s+estoy\s+(?:al|en el|cerca del)\s+borde\b",
    r"\bich\s+stehe\s+nicht\s+(?:am|an dem)\s+rand\b",
]


def _normalize(message):
    return re.sub(
        r"\s+",
        " ",
        unicodedata.normalize(
            "NFKC", message
        ).casefold(),
    ).strip()


def detect_crisis_rules(message: str) -> bool:
    if not isinstance(message, str):
        return False

    normalized = _normalize(message)

    return any(
        re.search(pattern, normalized, re.IGNORECASE)
        for pattern in CRISIS_PATTERNS
    )


def detect_unsafe_location(message: str) -> bool:
    if not isinstance(message, str):
        return False

    normalized = _normalize(message)

    if any(
        re.search(pattern, normalized)
        for pattern in NEGATED_UNSAFE_LOCATION_PATTERNS
    ):
        return False

    return any(
        re.search(pattern, normalized)
        for pattern in UNSAFE_LOCATION_PATTERNS
    )

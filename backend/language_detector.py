
"""
MindBridge AI - Multilingual Language Detector

Supported:
English, Urdu, Roman Urdu, Spanish, German.

Conservative heuristic detection.
Ambiguous text uses the selected fallback language.
"""

import re
import unicodedata

from language_registry import is_language_enabled


ROMAN_URDU_WORDS = {
    "mujhe", "mera", "meri", "mere",
    "main", "mein", "mai", "mujh",
    "nahi", "nahin", "kya", "kia",
    "hoon", "hun", "hai", "hain",
    "raha", "rahi", "rahe",
    "apni", "apna", "bohat", "bht",
    "kabhi", "lagta", "lagti",
    "chahiye", "karna", "karni",
    "mushkil", "haan", "han",
    "aap", "apko", "apki",
    "kaise", "kesay", "theek",
    "acha", "achha", "shukriya",
    "zaroor", "zaruri",
}

URDU_SPECIFIC_CHARS = set("ٹڈڑںھہۃےۓگچپژک")

URDU_WORDS = {
    "سلام", "مجھے", "میرا", "میری",
    "میرے", "آپ", "کیا", "کیسے",
    "کیوں", "نہیں", "ہے", "ہیں",
    "ہوں", "اور", "بہت",
    "پریشان", "اداس", "نیند",
    "مدد", "چاہیے", "رہا", "رہی",
}

ARABIC_WORDS = {
    "أنا", "أشعر", "اليوم",
    "كيف", "ماذا", "لماذا",
    "عندي", "أريد", "أحتاج",
    "التوتر", "القلق", "الحزن",
    "النوم", "شكرا",
}

SPANISH_WORDS = {
    "estoy", "siento", "sentirme", "tengo",
    "necesito", "ayuda", "hola", "gracias",
    "quiero", "puedo", "puedes",
    "hoy", "muy", "estresado",
    "estresada", "ansiedad", "triste",
    "tristeza", "seguro", "segura",
    "azotea", "borde", "techo",
    "vida", "hacerme", "daño",
    "respirar", "pecho", "dolor",
    "miedo", "solo", "sola",
    "siento", "hablar", "conmigo",
}

GERMAN_WORDS = {
    "ich", "bin", "heute", "sehr",
    "gestresst", "fühle", "mich",
    "nicht", "sicher", "hilfe",
    "brauche", "möchte", "habe",
    "angst", "traurig", "danke",
    "hallo", "kann", "bitte",
    "stehen", "stehe", "rand",
    "daches", "dach", "balkon",
    "leben", "beenden", "selbst",
    "verletzen", "schmerzen",
    "brust", "atmen", "schwer",
    "sprechen", "jemandem",
}

SPANISH_STRONG = {
    "estoy", "necesito", "ayuda",
    "estresado", "estresada",
    "azotea", "ansiedad", "quiero",
    "puedes", "hacerme",
}

GERMAN_STRONG = {
    "ich", "fühle", "gestresst",
    "brauche", "möchte", "nicht",
    "daches", "schmerzen",
    "verletzen", "beenden",
}


def _has_arabic_script(text):
    return any(
        0x0600 <= ord(char) <= 0x06FF
        for char in text
    )


def _detect_urdu(text):
    words = set(re.findall(r"[\u0600-\u06FF]+", text))

    urdu_score = len(words & URDU_WORDS)
    arabic_score = len(words & ARABIC_WORDS)

    if any(char in URDU_SPECIFIC_CHARS for char in text):
        urdu_score += 2

    return urdu_score > 0 and arabic_score == 0


def detect_language(message: str, fallback: str = "en") -> str:
    if not is_language_enabled(fallback):
        fallback = "en"

    if not isinstance(message, str):
        return fallback

    text = unicodedata.normalize(
        "NFKC", message.strip()
    ).casefold()

    if not text:
        return fallback

    if _has_arabic_script(text):
        if _detect_urdu(text) and is_language_enabled("ur"):
            return "ur"
        return fallback

    words = set(re.findall(r"[a-zà-ÿ]+", text))

    if words & ROMAN_URDU_WORDS:
        if is_language_enabled("roman_ur"):
            return "roman_ur"

    es_score = len(words & SPANISH_WORDS)
    de_score = len(words & GERMAN_WORDS)

    es_strong = bool(words & SPANISH_STRONG)
    de_strong = bool(words & GERMAN_STRONG)

    if (
        is_language_enabled("es")
        and es_score >= 2
        and es_strong
        and es_score > de_score
    ):
        return "es"

    if (
        is_language_enabled("de")
        and de_score >= 2
        and de_strong
        and de_score > es_score
    ):
        return "de"

    return fallback

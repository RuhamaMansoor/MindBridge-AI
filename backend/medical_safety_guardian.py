
"""
MindBridge AI - Medical Safety Guardian
Version: 0.6.1

Rule-based medical warning-sign screening.
Languages: English, Roman Urdu, Urdu script.

Not a diagnostic or clinically validated triage system.
A negative screen does not establish medical safety.
Uncertain cases require further review.
"""

from dataclasses import dataclass
import re
import unicodedata


@dataclass(frozen=True)
class MedicalSafetyResult:
    emergency_detected: bool
    category: str | None
    reason: str
    uncertain: bool = False


PRIORITY_CATEGORIES = (
    "stroke_warning",
    "sudden_vision_loss",
    "severe_eye_pain",
)

IMMEDIATE_CATEGORIES = set(PRIORITY_CATEGORIES)


# ------------------------------------------------------------
# Medical symptom detection
# ------------------------------------------------------------

PATTERNS = {
    "chest_pain": (
        r"\b(?:chest pain|chest pressure|pain (?:in|on) (?:my|the) chest|my chest (?:hurts|is hurting))\b",
        r"\b(?:seene|seenay|seena|chati|chaati)\b.{0,45}\b(?:dard|pain|dabao)\b",
        r"(?:سینے|چھاتی).{0,35}(?:درد|دباؤ)",
    ),

    "breathing_difficulty": (
        r"\b(?:shortness of breath|difficulty breathing|trouble breathing|can't breathe|cannot breathe|unable to breathe|struggling to breathe)\b",
        r"\b(?:saans|sans)\b.{0,45}\b(?:mushkil|takleef|nahi aa|nahin aa|ruk|phool)\w*",
        r"سانس.{0,35}(?:مشکل|تکلیف|نہیں آ|رک|پھول)",
    ),

    "sudden_vision_loss": (
        r"\b(?:sudden|suddenly|abruptly)\b.{0,90}\b(?:vision loss|loss of vision|blurred vision|blind|can't see|cannot see|unable to see)\b",
        r"\b(?:sudden|suddenly|abruptly)\b.{0,90}\b(?:lose|loses|losing|lost)\s+(?:(?:my|your|his|her|their|the)\s+)?(?:vision|sight|eyesight)\b",
        r"\b(?:vision loss|loss of vision|lost (?:my|his|her|their|the)?\s*vision|lost (?:my|his|her|their|the)?\s*sight)\b",
        r"\b(?:nazar|binai|binaai|roshni)\b.{0,75}\b(?:achanak|chali gayi|chali gai|khatam|band|nahi aa rahi|nahin aa rahi|nahi aa raha|nahin aa raha)\b",
        r"\bachanak\b.{0,85}\b(?:nazar|binai|binaai|roshni|dekh)\w*\b",
        r"\b(?:aankh|ankh|aankhon|ankhon)\b.{0,70}\b(?:roshni|nazar|binai|binaai)\b.{0,65}\b(?:chali gayi|chali gai|khatam|nahi aa rahi|nahin aa rahi)\b",
        r"\b(?:kuch|bilkul)\s+(?:nazar|dikhai|dikhayi)\s+(?:nahi|nahin)\s+(?:aa|de)\b",
        r"(?:نظر|بینائی|روشنی).{0,65}(?:اچانک|چلی گئی|ختم|بند|نہیں آ)",
        r"اچانک.{0,75}(?:نظر|بینائی|روشنی|دکھائی)",
        r"آنکھ.{0,60}(?:روشنی|نظر|بینائی).{0,55}(?:چلی گئی|ختم|نہیں آ)",
        r"(?:کچھ|بالکل).{0,20}(?:نظر|دکھائی).{0,20}نہیں",
    ),

    "severe_eye_pain": (
        r"\b(?:severe|intense|extreme|excruciating|unbearable)\b.{0,40}\b(?:eye pain|pain in (?:my|the) eye)\b",
        r"\b(?:eye pain|pain in (?:my|the) eye)\b.{0,40}\b(?:severe|intense|extreme|unbearable)\b",
        r"\b(?:aankh|ankh|aankhon|ankhon)\b.{0,50}\b(?:tez|shadeed|bohat|bardasht se bahar)\b.{0,35}\b(?:dard|pain)\b",
        r"\b(?:aankh|ankh|aankhon|ankhon)\b.{0,50}\b(?:dard|pain)\b.{0,35}\b(?:tez|shadeed|bohat)\b",
        r"(?:آنکھ|آنکھوں).{0,45}(?:شدید|تیز|بہت).{0,30}درد",
        r"(?:آنکھ|آنکھوں).{0,40}درد.{0,30}(?:شدید|تیز|ناقابل برداشت)",
    ),

    "stroke_warning": (
        r"\b(?:face drooping|facial droop|(?:my |his |her |their |the )?face (?:is|was|has been|started) (?:suddenly )?drooping|drooping (?:face|on one side of (?:my|the) face))\b",
        r"\b(?:slurred speech|(?:my |his |her |their |the )?speech (?:is|was|has become|became) (?:suddenly )?slurred|slurring (?:my|his|her|their)?\s*words)\b",
        r"\b(?:sudden one-sided weakness|sudden facial weakness)\b",
        r"\b(?:sudden|suddenly|abruptly)\b.{0,65}\b(?:cannot speak|can't speak|unable to speak|difficulty speaking|trouble speaking|cannot talk|can't talk|speech difficulty|one side (?:is )?weak|arm weakness)\b",
        r"\b(?:chehra|chehray)\b.{0,45}\b(?:latak\w*|tedha|terha)\b",
        r"\bachanak\b.{0,65}\b(?:bol\w*|baat)\b.{0,45}\b(?:mushkil|nahi|nahin|larakhara\w*)\b",
        r"\b(?:bolne|bolnay)\b.{0,40}\b(?:mushkil|larakhara\w*)\b",
        r"\bachanak\b.{0,60}\b(?:haath|hath|bazu|tang|pair)\b.{0,45}\b(?:kamzor|sunn|sun)\b",
        r"(?:چہرہ|چہرے).{0,40}(?:لٹک|ٹیڑھا)",
        r"بولنے.{0,40}(?:مشکل|لڑکھڑا)",
        r"اچانک.{0,55}(?:بول|بات).{0,35}(?:نہیں|مشکل)",
        r"اچانک.{0,55}(?:ہاتھ|بازو|ٹانگ|پیر).{0,40}(?:کمزور|سن)",
    ),
}


# ------------------------------------------------------------
# Spanish and German medical warning-sign patterns
# Add after PATTERNS and before NEGATIONS
# ------------------------------------------------------------

MULTILINGUAL_MEDICAL_PATTERNS = {
    "chest_pain": (
        # Spanish
        r"\b(?:dolor|presión|opresión)\b.{0,45}\b(?:pecho|torácic[oa])\b",
        r"\bpecho\b.{0,45}\b(?:duele|dolor|presión|opresión)\b",

        # German
        r"\b(?:brustschmerzen|brustschmerz|brustdruck|brustenge)\b",
        r"\b(?:schmerzen|druck|enge)\b.{0,35}\b(?:brust|brustkorb)\b",
    ),

    "breathing_difficulty": (
        # Spanish
        r"\b(?:dificultad|problemas)\s+para\s+respirar\b",
        r"\b(?:falta\s+de\s+aire|no\s+puedo\s+respirar|me\s+cuesta\s+respirar)\b",

        # German
        r"\b(?:atemnot|luftnot|atemprobleme)\b",
        r"\b(?:schwierigkeiten\s+beim\s+atmen|bekomme\s+keine\s+luft)\b",
        
        r"\b(?:bekomme|kriege)\s+(?:schlecht|kaum|schwer)\s+luft\b",
        r"\b(?:kann|könnte)\s+(?:nicht|kaum)\s+atmen\b",
        r"\b(?:schlecht|schwer)\s+luft\s+bekommen\b",

    ),

    "sudden_vision_loss": (
        r"\b(?:pérdida\s+repentina\s+de\s+(?:la\s+)?visión|perdí\s+(?:la\s+)?vista)\b",
        r"\b(?:plötzlicher\s+sehverlust|plötzlich\s+blind)\b",
    ),

    "severe_eye_pain": (
        r"\b(?:dolor\s+(?:muy\s+)?intenso\s+en\s+(?:el|los)\s+ojos?)\b",
        r"\b(?:starke|heftige)\s+augenschmerzen\b",
    ),

    "stroke_warning": (
        r"\b(?:habla\s+arrastrada|parálisis\s+facial\s+repentina)\b",
        r"\b(?:plötzlich\s+verwaschene\s+sprache|plötzliche\s+gesichtslähmung)\b",
    ),
}

for category, extra_patterns in MULTILINGUAL_MEDICAL_PATTERNS.items():
    PATTERNS[category] = (
        *PATTERNS[category],
        *extra_patterns,
    )

# ------------------------------------------------------------
# Explicit negations
# ------------------------------------------------------------

NEGATIONS = {
    "chest_pain": (
        r"\b(?:no chest pain|not having chest pain|(?:i )?(?:do not|don't|did not|didn't) have chest pain)\b",
        r"\b(?:seene|seenay|seena|chati|chaati)\b.{0,35}\b(?:dard|pain|dabao)\b.{0,15}\b(?:nahi|nahin)\b",
        r"(?:سینے|چھاتی).{0,30}(?:درد|دباؤ).{0,15}نہیں",
    ),

    "breathing_difficulty": (
        r"\b(?:no difficulty breathing|not having trouble breathing|no trouble breathing)\b",
        r"\b(?:saans|sans)\b.{0,35}\b(?:mushkil|takleef)\b.{0,15}\b(?:nahi|nahin)\b",
        r"سانس.{0,30}(?:مشکل|تکلیف).{0,15}نہیں",
    ),

    "sudden_vision_loss": (
        r"\b(?:no vision loss|(?:koi )?vision loss (?:nahi|nahin)(?: hai)?|not losing (?:my )?vision|vision is fine|my (?:vision|eyesight) is (?:fine|normal))\b",
        r"\b(?:nazar|binai|binaai|roshni)\b.{0,25}\b(?:theek|sahi|normal)\b",
        r"(?:نظر|بینائی|روشنی).{0,20}(?:ٹھیک|صحیح)",
    ),

    "severe_eye_pain": (
        r"\b(?:no (?:severe )?eye pain|not having eye pain)\b",
        r"\b(?:aankh|ankh|aankhon|ankhon)\b.{0,30}\b(?:dard|pain)\b.{0,15}\b(?:nahi|nahin)\b",
        r"آنکھ.{0,30}درد.{0,15}نہیں",
    ),

    "stroke_warning": (
        r"\b(?:no slurred speech|speech is normal|can speak normally|face is not drooping|my face is normal)\b",
    ),
    
    
}


# ------------------------------------------------------------
# Context patterns
# ------------------------------------------------------------

ACUTE_PATTERN = re.compile(
    r"\b(?:sudden|suddenly|abruptly|severe|intense|"
    r"right now|currently|today|abhi|achanak|"
    r"bohat tez|shadeed|foran)\b|"
    r"اچانک|ابھی|آج|شدید|بہت تیز",
    re.IGNORECASE,
)

HYPOTHETICAL_PATTERN = re.compile(
    r"^\s*(?:what if|suppose|hypothetically|"
    r"for example|imagine|agar kisi|agar koi|"
    r"farz karein|مثال کے طور پر|"
    r"فرض کریں|اگر کسی)",
    re.IGNORECASE,
)

HISTORICAL_PATTERN = re.compile(
    r"\b(?:last year|years ago|months ago|"
    r"in the past|used to have|pichlay saal|"
    r"pichle saal|pehle hota tha)\b|"
    r"پچھلے سال|گزشتہ سال",
    re.IGNORECASE,
)

CLAUSE_SPLIT_PATTERN = (
    r"\b(?:but|however|lekin|magar)\b|"
    r"(?:لیکن|مگر)|[.;،؛]"
)

SEVERE_BREATHING_PATTERN = re.compile(
    r"\b(?:cannot breathe|can't breathe|"
    r"unable to breathe|struggling to breathe|"
    r"saans nahi aa|saans nahin aa)\b|"
    r"سانس نہیں آ",
    re.IGNORECASE,
)

SEVERITY_PATTERN = re.compile(
    r"\b(?:bohat|bahut|shadeed|tez|severe|"
    r"extreme|intense)\b|بہت|شدید",
    re.IGNORECASE,
)


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def normalize_text(message: str) -> str:
    text = unicodedata.normalize("NFKC", message)
    text = re.sub(r"[\u064b-\u065f\u0670]", "", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def _matches(text: str, category: str) -> bool:
    return any(
        re.search(pattern, text, re.IGNORECASE)
        for pattern in PATTERNS[category]
    )


def _matched_categories(text: str) -> list[str]:
    return [
        category
        for category in PATTERNS
        if _matches(text, category)
    ]


def _is_hypothetical(text: str) -> bool:
    return bool(HYPOTHETICAL_PATTERN.search(text))


def _is_historical(text: str) -> bool:
    return bool(HISTORICAL_PATTERN.search(text))


def _is_acute(text: str) -> bool:
    return bool(ACUTE_PATTERN.search(text))


def _split_clauses(text: str) -> list[str]:
    parts = re.split(
        CLAUSE_SPLIT_PATTERN,
        text,
        flags=re.IGNORECASE,
    )

    return [
        part.strip(" ,.;،؛")
        for part in parts
        if part.strip(" ,.;،؛")
    ]


def _remove_negated_symptoms(
    clause: str,
) -> tuple[str, set[str]]:
    """
    Remove explicit negative symptom phrases while
    preserving other positive symptoms.
    """
    masked = clause
    negated_categories = set()

    for category, patterns in NEGATIONS.items():
        for pattern in patterns:
            if re.search(pattern, masked, re.IGNORECASE):
                negated_categories.add(category)
                masked = re.sub(
                    pattern,
                    " ",
                    masked,
                    flags=re.IGNORECASE,
                )

    return masked, negated_categories


# ------------------------------------------------------------
# Main assessment
# ------------------------------------------------------------

def assess_medical_safety(message: str) -> MedicalSafetyResult:
    """
    Screen configured medical warning signs.

    emergency_detected=False does not establish safety.
    """

    if not isinstance(message, str):
        raise TypeError("message must be a string")

    text = normalize_text(message)

    if not text:
        return MedicalSafetyResult(
            False,
            None,
            "Empty message",
        )

    # 1. Hypothetical context
    hypothetical = _is_hypothetical(text)

    first_person_current = bool(
        re.search(
            r"\b(?:i am|i'm|my (?:face|eye|vision|chest)|"
            r"mujhe|meri|mera|mere)\b|"
            r"مجھے|میری|میرا",
            text,
        )
    )

    if hypothetical and not first_person_current:
        matched = _matched_categories(text)

        if matched:
            category = next(
                (
                    item
                    for item in PRIORITY_CATEGORIES
                    if item in matched
                ),
                matched[0],
            )

            return MedicalSafetyResult(
                False,
                category,
                "Hypothetical question requires contextual review",
                True,
            )

    # 2. Analyze symptoms and negations
    active = set()
    uncertain = set()

    for clause in _split_clauses(text):
        cleaned, negated_categories = _remove_negated_symptoms(
            clause
        )

        matched = _matched_categories(cleaned)

        if _is_historical(clause):
            uncertain.update(matched)
        else:
            active.update(matched)

        uncertain.update(negated_categories)

    # 3. Immediate medical warnings
    for category in PRIORITY_CATEGORIES:
        if category in active:
            return MedicalSafetyResult(
                True,
                category,
                "Potential urgent medical red flag",
                False,
            )

    # 4. Combined chest pain and breathing difficulty
    # This must be checked before breathing-only severity.
    if {
        "chest_pain",
        "breathing_difficulty",
    }.issubset(active):
        return MedicalSafetyResult(
            True,
            "cardiorespiratory_emergency",
            "Chest pain with breathing difficulty",
            False,
        )

    # 5. Severe breathing difficulty
    if "breathing_difficulty" in active:
        if (
            SEVERE_BREATHING_PATTERN.search(text)
            or SEVERITY_PATTERN.search(text)
        ):
            return MedicalSafetyResult(
                True,
                "breathing_difficulty",
                "Potentially severe breathing difficulty",
                False,
            )

    # 6. Acute symptoms
    if active and _is_acute(text):
        category = next(
            item
            for item in PATTERNS
            if item in active
        )

        return MedicalSafetyResult(
            True,
            category,
            "Acute medical red-flag symptom",
            False,
        )

    # 7. Contextual review
    if active or uncertain:
        category = next(
            item
            for item in PATTERNS
            if item in active or item in uncertain
        )

        return MedicalSafetyResult(
            False,
            category,
            "Medical symptoms require contextual review",
            True,
        )

    # 8. No configured red flag
    return MedicalSafetyResult(
        False,
        None,
        "No configured red flag matched",
        False,
    )

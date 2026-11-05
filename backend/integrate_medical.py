
"""
MindBridge AI - Medical Guardian Integration
Version: 1.0

Updates existing main.py while preserving its
session, language, AWS and OpenAI workflows.

Creates a backup before replacing main.py.
"""

from pathlib import Path
import ast
import shutil


MAIN = Path(__file__).resolve().parent / "main.py"

if not MAIN.is_file():
    raise SystemExit(
        "main.py not found in the same folder."
    )

source = MAIN.read_text(encoding="utf-8-sig")

if (
    "from medical_safety_guardian import assess_medical_safety"
    in source
):
    raise SystemExit(
        "Medical Guardian already appears integrated. "
        "No changes made."
    )


# ==================================================
# 1. Localized Emergency Responses
# ==================================================

medical_code = '''
MEDICAL_EMERGENCY_MESSAGES = {
    "en": {
        "general": (
            "These symptoms may be a medical emergency. "
            "Call your local emergency number now and "
            "request an ambulance. Do not drive yourself. "
            "Ask someone nearby to stay with you."
        ),
        "eye": (
            "Sudden vision changes or severe eye pain "
            "need immediate emergency assessment. "
            "Go to an emergency department now; "
            "do not wait for a routine appointment. "
            "Do not drive yourself."
        ),
        "stroke": (
            "Sudden speech difficulty, facial drooping "
            "or one-sided weakness may be signs of a stroke. "
            "Call your local emergency number now and "
            "request an ambulance. Do not drive yourself. "
            "Note when symptoms began if known."
        ),
    },
    "roman_ur": {
        "general": (
            "Yeh alamat medical emergency ho sakti hain. "
            "Abhi local emergency number par call karke "
            "ambulance bulayein. Khud drive na karein. "
            "Kisi bharosemand shakhs ko apne paas bulayein."
        ),
        "eye": (
            "Achanak nazar mein tabdeeli ya aankh mein "
            "shadeed dard ke liye foran emergency medical "
            "assessment zaroori hai. Abhi emergency "
            "department jayein; routine appointment ka "
            "intezar na karein. Khud drive na karein."
        ),
        "stroke": (
            "Achanak bolne mein mushkil, chehre ka latakna "
            "ya jism ki ek taraf kamzori stroke ki alamat "
            "ho sakti hai. Abhi local emergency number par "
            "call karke ambulance bulayein. Khud drive "
            "na karein. Alamat shuru hone ka waqt note "
            "karein agar maloom ho."
        ),
    },
    "ur": {
        "general": (
            "یہ علامات طبی ایمرجنسی ہو سکتی ہیں۔ "
            "ابھی مقامی ایمرجنسی نمبر پر کال کر کے "
            "ایمبولینس بلائیں۔ خود گاڑی نہ چلائیں۔ "
            "کسی قابلِ اعتماد شخص کو پاس بلائیں۔"
        ),
        "eye": (
            "اچانک نظر میں تبدیلی یا آنکھ میں شدید درد "
            "کے لیے فوری طبی معائنہ ضروری ہے۔ "
            "ابھی ایمرجنسی ڈیپارٹمنٹ جائیں، معمول کی "
            "اپائنٹمنٹ کا انتظار نہ کریں۔ "
            "خود گاڑی نہ چلائیں۔"
        ),
        "stroke": (
            "اچانک بولنے میں مشکل، چہرے کا لٹکنا یا "
            "جسم کے ایک طرف کمزوری فالج کی علامت "
            "ہو سکتی ہے۔ ابھی مقامی ایمرجنسی نمبر پر "
            "کال کر کے ایمبولینس بلائیں۔ "
            "خود گاڑی نہ چلائیں۔ اگر معلوم ہو تو "
            "علامات شروع ہونے کا وقت نوٹ کریں۔"
        ),
    },
}


def medical_emergency_text(
    category: str | None,
    language: str,
) -> str:
    messages = MEDICAL_EMERGENCY_MESSAGES.get(
        language,
        MEDICAL_EMERGENCY_MESSAGES["en"],
    )

    if category == "stroke_warning":
        return messages["stroke"]

    if category in {
        "sudden_vision_loss",
        "severe_eye_pain",
    }:
        return messages["eye"]

    return messages["general"]


'''


# ==================================================
# 2. Safe Replacement Helper
# ==================================================

def replace_once(old: str, new: str) -> None:
    global source

    count = source.count(old)

    if count != 1:
        raise RuntimeError(
            f"Expected one insertion point, "
            f"found {count}: {old[:65]!r}"
        )

    source = source.replace(
        old,
        new,
        1,
    )


# ==================================================
# 3. Add Medical Guardian Import
# ==================================================

replace_once(
    "from conversation_store import conversation_store",
    (
        "from conversation_store import conversation_store\n"
        "from medical_safety_guardian import "
        "assess_medical_safety"
    ),
)


# ==================================================
# 4. Correct Language Registry Compatibility
# ==================================================

replace_once(
    (
        "SUPPORTED_LANGUAGES = set(\n"
        "    get_enabled_languages().keys()\n"
        ")"
    ),
    (
        "_enabled_languages = get_enabled_languages()\n"
        "SUPPORTED_LANGUAGES = set(_enabled_languages)"
    ),
)


# ==================================================
# 5. Add Emergency Response Registry
# ==================================================

replace_once(
    "app = FastAPI(",
    medical_code + "app = FastAPI(",
)


# ==================================================
# 6. Add Medical Screening Before AI Calls
# ==================================================

save_message_marker = (
    "    # ----------------------------------------------\n"
    "    # D. Save User Message"
)

medical_check = '''    # Medical screening before external AI calls.
    # A negative screen is NOT medical clearance.

    medical_result = None

    try:
        medical_result = assess_medical_safety(
            message
        )

    except Exception:
        logger.exception(
            "Medical safety screening failed"
        )

'''

replace_once(
    save_message_marker,
    medical_check + save_message_marker,
)


# ==================================================
# 7. Emergency Guidance During AWS Failure
# ==================================================

failure_marker = '''        if pending_safety:
            return respond(
                safety_reply("fallback"),
                pending=True,
            )

        return respond(
            safety_reply("fallback"),
            concern_type="assessment_unavailable",
        )'''

medical_failure = '''        if (
            medical_result is not None
            and medical_result.emergency_detected
        ):
            return respond(
                medical_emergency_text(
                    medical_result.category,
                    language,
                )
            )

'''

replace_once(
    failure_marker,
    medical_failure + failure_marker,
)


# ==================================================
# 8. Add Medical Emergency Route
# ==================================================

followup_marker = '''    # ----------------------------------------------
    # H. Pending Safety Follow-up'''

medical_route = '''    # ----------------------------------------------
    # G1. Medical Emergency Handling
    # ----------------------------------------------

    if (
        medical_result is not None
        and medical_result.emergency_detected
    ):
        logger.warning(
            "Medical emergency route triggered: %s",
            medical_result.category,
        )

        return respond(
            medical_emergency_text(
                medical_result.category,
                language,
            )
        )

'''

replace_once(
    followup_marker,
    medical_route + followup_marker,
)


# ==================================================
# 9. Validate Before Writing
# ==================================================

ast.parse(
    source,
    filename="main.py",
)


# ==================================================
# 10. Backup Original and Save Updated main.py
# ==================================================

backup = MAIN.with_name(
    "main_before_medical_integration.py"
)

if backup.exists():
    raise SystemExit(
        "Backup already exists. No files changed. "
        "Move or rename it before retrying."
    )

shutil.copy2(
    MAIN,
    backup,
)

MAIN.write_text(
    source,
    encoding="utf-8",
)

print("Integration complete.")
print("Backup:", backup)
print("Updated:", MAIN)

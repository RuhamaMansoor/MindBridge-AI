
"""
MindBridge AI - Multilingual Safety Responses

Languages:
- English
- Roman Urdu
- Urdu
- Spanish
- German

All emergency responses are predefined.
Draft translations require native-language and
clinical review before production activation.
"""

from language_detector import detect_language
from language_registry import get_enabled_languages
from safety_translations_extra import EXTRA_SAFETY_MESSAGES


# ==================================================
# 1. Main Safety Messages
# ==================================================

SAFETY_MESSAGES = {
    "en": {
        "crisis": (
            "I'm concerned about your immediate safety. "
            "Please contact local emergency services or go to "
            "the nearest emergency department now. "
            "If you can do so safely, move away from anything "
            "you could use to hurt yourself. "
            "Ask a trusted person to stay with you and help "
            "you get urgent support. "
            "Are you somewhere safe right now?"
        ),
        "crisis_ongoing": (
            "I'm concerned because you've told me you're "
            "still unsafe. Please call local emergency "
            "services now and tell them you need immediate "
            "help. If you can do so safely, move away from "
            "any dangerous location or anything you could "
            "use to hurt yourself. Contact someone you trust "
            "and ask them to come stay with you. "
            "You do not have to manage this alone."
        ),
        "clarification": (
            "Thank you for sharing how you're feeling. "
            "I want to understand your safety. "
            "Are you thinking about harming yourself "
            "right now? If you're in immediate danger, "
            "contact emergency services and ask "
            "someone you trust to stay with you."
        ),
        "followup": (
            "Thank you for being open with me. "
            "Are you thinking of acting on these thoughts "
            "now, or have you made a plan? "
            "If you might act on them, please contact "
            "emergency services immediately and ask "
            "a trusted person to stay with you."
        ),
        "fallback": (
            "I'm unable to reliably assess your situation "
            "right now. If you're in immediate danger, "
            "contact local emergency services or go to "
            "the nearest emergency department. "
            "You can also reach out to someone you trust "
            "or a qualified mental health professional."
        ),
        "escalation": (
            "Thank you for continuing to talk with me. "
            "I'm still concerned about your safety, "
            "and I don't want to keep repeating the same "
            "questions. Please reach out to a qualified "
            "mental health professional or someone you trust. "
            "If you might harm yourself or someone else, "
            "contact local emergency services or go to "
            "the nearest emergency department immediately. "
            "You can continue talking with me, but I cannot "
            "replace professional or emergency support."
        ),
        "service_unavailable": (
            "MindBridge AI is having trouble responding "
            "right now. Please try again shortly. "
            "If you are in immediate danger, contact "
            "local emergency services or go to the "
            "nearest emergency department."
        ),
    },

    "roman_ur": {
        "crisis": (
            "Mujhe aap ki foran safety ki fikr hai. "
            "Barah-e-karam abhi local emergency services "
            "se rabta karein ya qareebi hospital ke "
            "emergency department jayein. "
            "Agar mehfooz tareeqay se mumkin ho, to un "
            "cheezon se door ho jayein jin se aap apne "
            "aap ko nuqsan pohancha sakte hain. "
            "Kisi bharosemand shakhs ko apne paas bulayein. "
            "Kya aap is waqt kisi mehfooz jagah par hain?"
        ),
        "crisis_ongoing": (
            "Mujhe aap ki safety ki abhi bhi fikr hai, "
            "kyunki aap ne bataya hai ke aap mehfooz nahi hain. "
            "Barah-e-karam abhi local emergency services ko "
            "call karein aur batayein ke aap ko foran madad "
            "chahiye. Agar mehfooz tareeqay se mumkin ho, "
            "to khatarnak jagah aur un cheezon se door "
            "ho jayein jin se aap ko nuqsan pohanch sakta hai. "
            "Kisi bharosemand shakhs ko apne paas bulayein "
            "aur unse apne saath rehne ko kahein."
        ),
       
        "clarification": (
            "Aap ne jo bataya hai, main use sanjeedgi se "
            "le raha hoon. Mujhe aap ki safety ki fikr hai. "
            "Agar aap ko lagta hai ke aap apne aap ko "
            "nuqsan pohancha sakte hain, to barah-e-karam "
            "abhi akelay na rahein. Kisi bharosemand "
            "shakhs ko call karein aur unhein apne paas "
            "aane ya apne saath rehne ko kahein. "
            "Agar mehfooz tareeqay se mumkin ho, to "
            "aisi cheezon se door ho jayein jin se "
            "aap apne aap ko nuqsan pohancha sakte hain. "
            "Agar foran khatra hai, to abhi local "
            "emergency services se rabta karein ya "
            "qareebi emergency department se madad lein. "
            "Kya aap ko lagta hai ke aap is waqt "
            "apne aap ko nuqsan pohancha sakte hain?"
        ),

        "followup": (
            "Shukriya ke aap ne apni baat share ki. "
            "Kya aap is waqt in khayalat par amal karne "
            "ka irada rakhte hain, ya koi plan banaya hai? "
            "Agar foran khatra hai to emergency services "
            "se rabta karein aur kisi bharosemand shakhs "
            "ko apne paas bulayein."
        ),
        "fallback": (
            "Main is waqt aap ki situation ka reliable "
            "assessment nahi kar pa raha. "
            "Agar aap ko foran khatra hai to local "
            "emergency services ya nearest emergency "
            "department se rabta karein. "
            "Kisi bharosemand shakhs ya qualified mental "
            "health professional se bhi baat kar sakte hain."
        ),
        "escalation": (
            "Shukriya ke aap mujhse baat kar rahe hain. "
            "Mujhe abhi bhi aap ki safety ki fikr hai, "
            "aur main baar baar wahi sawal nahi poochna chahta. "
            "Barah-e-karam kisi qualified mental health "
            "professional ya bharosemand shakhs se rabta karein. "
            "Agar foran khatra hai to local emergency services "
            "ya nearest emergency department se rabta karein. "
            "Main professional ya emergency support ka "
            "replacement nahi hoon."
        ),
        "service_unavailable": (
            "MindBridge AI ko is waqt jawab dene mein "
            "technical problem aa rahi hai. "
            "Barah-e-karam thori dair baad dobara try karein. "
            "Agar aap ko foran khatra hai, to local emergency "
            "services ya nearest emergency department se "
            "rabta karein."
        ),
    },

    "ur": {
        "crisis": (
            "مجھے آپ کی فوری حفاظت کی فکر ہے۔ "
            "براہِ کرم ابھی مقامی ایمرجنسی سروسز سے رابطہ کریں "
            "یا قریبی ہسپتال کے ایمرجنسی ڈیپارٹمنٹ جائیں۔ "
            "اگر محفوظ طریقے سے ممکن ہو تو ایسی چیزوں سے دور "
            "ہو جائیں جن سے آپ خود کو نقصان پہنچا سکتے ہیں۔ "
            "کسی قابلِ اعتماد شخص کو اپنے پاس بلائیں۔ "
            "کیا آپ اس وقت کسی محفوظ جگہ پر ہیں؟"
        ),
        "crisis_ongoing": (
            "مجھے اب بھی آپ کی حفاظت کی فکر ہے کیونکہ "
            "آپ نے بتایا ہے کہ آپ محفوظ نہیں ہیں۔ "
            "براہِ کرم ابھی مقامی ایمرجنسی سروسز کو فون کریں "
            "اور بتائیں کہ آپ کو فوری مدد کی ضرورت ہے۔ "
            "اگر محفوظ طریقے سے ممکن ہو تو خطرناک جگہ "
            "اور ایسی چیزوں سے دور ہو جائیں جن سے "
            "آپ کو نقصان پہنچ سکتا ہے۔ "
            "کسی قابلِ اعتماد شخص کو فوراً اپنے پاس بلائیں "
            "اور ان سے اپنے ساتھ رہنے کو کہیں۔"
        ),
        "clarification": (
            "اپنے احساسات بتانے کا شکریہ۔ "
            "کیا آپ اس وقت خود کو نقصان پہنچانے "
            "کے بارے میں سوچ رہے ہیں؟ "
            "اگر فوری خطرہ ہے تو ایمرجنسی سروسز سے "
            "رابطہ کریں اور کسی قابلِ اعتماد شخص "
            "کو اپنے پاس بلائیں۔"
        ),
        "followup": (
            "آپ کی بات شیئر کرنے کا شکریہ۔ "
            "کیا آپ اس وقت ان خیالات پر عمل کرنے "
            "کا ارادہ رکھتے ہیں، یا آپ نے کوئی "
            "منصوبہ بنایا ہے؟ "
            "اگر فوری خطرہ ہے تو ایمرجنسی سروسز سے "
            "رابطہ کریں اور کسی قابلِ اعتماد شخص "
            "کو اپنے پاس بلائیں۔"
        ),
        "fallback": (
            "میں اس وقت آپ کی صورتحال کا قابلِ اعتماد "
            "اندازہ نہیں لگا پا رہا۔ "
            "اگر فوری خطرہ ہے تو مقامی ایمرجنسی "
            "سروسز سے رابطہ کریں یا قریبی ایمرجنسی "
            "ڈیپارٹمنٹ جائیں۔ "
            "کسی قابلِ اعتماد شخص یا ماہرِ نفسیاتی "
            "صحت سے بھی رابطہ کریں۔"
        ),
        "escalation": (
            "آپ کا مجھ سے بات جاری رکھنے کا شکریہ۔ "
            "مجھے اب بھی آپ کی حفاظت کے بارے میں تشویش ہے، "
            "اور میں بار بار ایک ہی سوال نہیں پوچھنا چاہتا۔ "
            "براہِ کرم کسی مستند ماہرِ نفسیاتی صحت یا "
            "قابلِ اعتماد شخص سے رابطہ کریں۔ "
            "اگر فوری خطرہ ہے تو مقامی ایمرجنسی سروسز "
            "سے رابطہ کریں یا قریبی ایمرجنسی ڈیپارٹمنٹ جائیں۔ "
            "میں پیشہ ورانہ یا ہنگامی مدد کا متبادل نہیں ہوں۔"
        ),
        "service_unavailable": (
            "MindBridge AI کو اس وقت جواب دینے میں "
            "تکنیکی دشواری پیش آ رہی ہے۔ "
            "براہِ کرم تھوڑی دیر بعد دوبارہ کوشش کریں۔ "
            "اگر فوری خطرہ ہے تو مقامی ایمرجنسی "
            "سروسز سے رابطہ کریں یا قریبی "
            "ایمرجنسی ڈیپارٹمنٹ جائیں۔"
        ),
    },
}


# ==================================================
# 2. Additional Language Translations
# ==================================================

# Preserve existing Spanish and German messages.
SAFETY_MESSAGES.update(EXTRA_SAFETY_MESSAGES)


# ==================================================
# 3. Unsafe Location Responses - All 5 Languages
# ==================================================

UNSAFE_LOCATION_MESSAGES = {
    "en": (
        "I'm concerned that you may be in immediate danger. "
        "If you can do so safely, move away from the edge "
        "and go somewhere safer, away from the height. "
        "Call local emergency services now and tell them "
        "your exact location. Ask someone you trust to come "
        "and stay with you. Are you away from the edge now?"
    ),
    "roman_ur": (
        "Mujhe fikr hai ke aap is waqt foran khatray mein "
        "ho sakte hain. Agar mehfooz tareeqay se mumkin ho, "
        "to kinare se door ho kar kisi mehfooz jagah par "
        "chalay jayein. Abhi local emergency services ko "
        "call karein aur apni exact location batayein. "
        "Kisi bharosemand shakhs ko apne paas bulayein. "
        "Kya aap ab kinare se door hain?"
    ),
    "ur": (
        "مجھے فکر ہے کہ آپ اس وقت فوری خطرے میں ہو سکتے ہیں۔ "
        "اگر محفوظ طریقے سے ممکن ہو تو کنارے سے دور ہو کر "
        "کسی محفوظ جگہ چلے جائیں۔ ابھی مقامی ایمرجنسی "
        "سروسز کو فون کریں اور اپنی درست جگہ بتائیں۔ "
        "کسی قابلِ اعتماد شخص کو اپنے پاس بلائیں۔ "
        "کیا آپ اب کنارے سے دور ہیں؟"
    ),
    "es": (
        "Me preocupa que puedas estar en peligro inmediato. "
        "Si puedes hacerlo de forma segura, aléjate del borde "
        "y dirígete a un lugar más seguro, lejos de la altura. "
        "Llama ahora a los servicios de emergencia locales "
        "e indica tu ubicación exacta. Pide a una persona "
        "de confianza que venga y se quede contigo. "
        "¿Ya estás lejos del borde?"
    ),
    "de": (
        "Ich mache mir Sorgen, dass Sie in unmittelbarer "
        "Gefahr sein könnten. Wenn es gefahrlos möglich ist, "
        "entfernen Sie sich vom Rand und gehen Sie an einen "
        "sichereren Ort, weg von der Höhe. "
        "Rufen Sie jetzt den örtlichen Notruf an und "
        "teilen Sie Ihren genauen Standort mit. "
        "Bitten Sie eine vertraute Person, zu Ihnen zu "
        "kommen und bei Ihnen zu bleiben. "
        "Sind Sie jetzt vom Rand entfernt?"
    ),
}

for language_code, response_text in UNSAFE_LOCATION_MESSAGES.items():
    SAFETY_MESSAGES[language_code]["unsafe_location"] = response_text


# ==================================================
# 4. Required Safety Response Types
# ==================================================

REQUIRED_SAFETY_TYPES = {
    "crisis",
    "crisis_ongoing",
    "unsafe_location",
    "clarification",
    "followup",
    "fallback",
    "escalation",
    "service_unavailable",
}


# ==================================================
# 5. Localization Validation
# ==================================================

def validate_safety_localizations() -> None:
    """
    Validate every defined language and every
    required safety response type.
    """

    for language_code, messages in SAFETY_MESSAGES.items():
        missing = REQUIRED_SAFETY_TYPES - set(messages.keys())

        if missing:
            raise RuntimeError(
                f"Missing safety responses for "
                f"{language_code}: {sorted(missing)}"
            )

        for response_type in REQUIRED_SAFETY_TYPES:
            response_text = messages[response_type]

            if (
                not isinstance(response_text, str)
                or not response_text.strip()
            ):
                raise RuntimeError(
                    f"Invalid safety response: "
                    f"{language_code}/{response_type}"
                )

    for language_code in get_enabled_languages():
        if language_code not in SAFETY_MESSAGES:
            raise RuntimeError(
                f"Enabled language has no safety messages: "
                f"{language_code}"
            )


# ==================================================
# 6. Safety Response by Detected Language
# ==================================================

def get_safety_response(
    response_type: str,
    message: str,
) -> str:
    language = detect_language(message)

    if language not in get_enabled_languages():
        language = "en"

    messages = SAFETY_MESSAGES[language]

    return messages.get(
        response_type,
        messages["fallback"],
    )


# ==================================================
# 7. Safety Response by Selected Language
# ==================================================

def get_safety_response_by_language(
    response_type: str,
    language: str,
) -> str:
    if language not in get_enabled_languages():
        language = "en"

    messages = SAFETY_MESSAGES[language]

    return messages.get(
        response_type,
        messages["fallback"],
    )


# ==================================================
# 8. Startup Validation
# ==================================================

validate_safety_localizations()

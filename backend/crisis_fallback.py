
"""
MindBridge AI - Independent Crisis Fallback
Version: 0.2.1

Purpose:
Provide limited rule-based crisis detection
when the AWS safety assessment is unavailable.

Supported:
- English
- Roman Urdu
- Urdu

IMPORTANT:
This is NOT a clinical risk assessment.
A negative result does not establish safety.
"""

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class CrisisFallbackResult:
    explicit_crisis: bool
    reason: str
    uncertain: bool = True


# ==================================================
# 1. EXPLICIT CRISIS PATTERNS
# ==================================================

CRISIS_PATTERNS = [

    # ----------------------------------------------
    # ENGLISH
    # ----------------------------------------------

    r"\bi\s+am\s+planning\s+to\s+kill\s+myself\b",
    r"\bi\s+am\s+planning\s+to\s+end\s+my\s+life\b",

    r"\bi'm\s+planning\s+to\s+kill\s+myself\b",
    r"\bi'm\s+planning\s+to\s+end\s+my\s+life\b",

    r"\bi\s+want\s+to\s+die\b",
    r"\bi\s+want\s+to\s+kill\s+myself\b",
    r"\bi\s+want\s+to\s+end\s+my\s+life\b",

    r"\bi\s+am\s+going\s+to\s+kill\s+myself\b",
    r"\bi\s+am\s+going\s+to\s+end\s+my\s+life\b",

    r"\bi'm\s+going\s+to\s+kill\s+myself\b",
    r"\bi'm\s+going\s+to\s+end\s+my\s+life\b",

    r"\bi\s+will\s+kill\s+myself\b",
    r"\bi\s+will\s+end\s+my\s+life\b",

    r"\bi\s+have\s+(?:a\s+)?plan\s+to\s+kill\s+myself\b",
    r"\bi\s+have\s+(?:a\s+)?plan\s+to\s+end\s+my\s+life\b",

    r"\bi\s+intend\s+to\s+kill\s+myself\b",
    r"\bi\s+intend\s+to\s+end\s+my\s+life\b",

    r"\bi\s+(?:might|may)\s+kill\s+myself\b",

    r"\bi\s+am\s+about\s+to\s+kill\s+myself\b",
    r"\bi\s+am\s+about\s+to\s+hurt\s+myself\b",

    r"\bi\s+want\s+to\s+hurt\s+myself\b",

    r"\bi\s+am\s+thinking\s+about\s+suicide\b",
    r"\bi\s+am\s+thinking\s+about\s+killing\s+myself\b",

    r"\bi\s+am\s+suicidal\b",

    # ----------------------------------------------
    # ROMAN URDU
    # ----------------------------------------------

    r"\bmain\s+khudkushi\s+karna\s+chaht[ai]\s+hoon\b",

    r"\bmain\s+khudkushi\s+kar\s+loon\s+g[ai]\b",

    r"\bmain\s+apni\s+jaan\s+lena\s+chaht[ai]\s+hoon\b",

    r"\bmain\s+apni\s+jaan\s+le\s+loon\s+g[ai]\b",

    r"\bmain\s+khud\s+ko\s+maar\s+dalna\s+chaht[ai]\s+hoon\b",

    r"\bmain\s+khud\s+ko\s+maar\s+daloon\s+g[ai]\b",

    r"\bmujhe\s+khudkushi\s+karni\s+hai\b",

    r"\bmain\s+marna\s+chaht[ai]\s+hoon\b",

    r"\bmujhe\s+marna\s+hai\b",

    # ----------------------------------------------
    # URDU
    # ----------------------------------------------

    r"میں\s+خودکشی\s+کرنا\s+چاہت[ای]\s+ہوں",

    r"میں\s+اپنی\s+جان\s+لینا\s+چاہت[ای]\s+ہوں",

    r"میں\s+خود\s+کو\s+مارنا\s+چاہت[ای]\s+ہوں",

    r"مجھے\s+خودکشی\s+کرنی\s+ہے",

    r"میں\s+مرنا\s+چاہت[ای]\s+ہوں",

    r"مجھے\s+مرنا\s+ہے",

    # ----------------------------------------------
    # GERMAN
    # ----------------------------------------------

    r"\bich\s+will\s+sterben\b",
    r"\bich\s+möchte\s+sterben\b",
    r"\bich\s+möchte\s+nicht\s+mehr\s+leben\b",
    r"\bich\s+will\s+nicht\s+mehr\s+leben\b",

    r"\bich\s+will\s+mich\s+umbringen\b",
    r"\bich\s+möchte\s+mich\s+umbringen\b",
    r"\bich\s+werde\s+mich\s+umbringen\b",

    r"\bich\s+will\s+mir\s+das\s+leben\s+nehmen\b",
    r"\bich\s+werde\s+mir\s+das\s+leben\s+nehmen\b",

    r"\bich\s+denke\s+an\s+suizid\b",
    r"\bich\s+denke\s+an\s+selbstmord\b",

    r"\bich\s+habe\s+suizidgedanken\b",

    r"\bich\s+will\s+mir\s+wehtun\b",
    r"\bich\s+möchte\s+mir\s+wehtun\b",
    r"\bich\s+könnte\s+mir\s+etwas\s+antun\b",

    r"\bich\s+habe\s+vor\s+mich\s+umzubringen\b",

    # ----------------------------------------------
    # SPANISH
    # ----------------------------------------------

    r"\bquiero\s+morir\b",
    r"\bme\s+quiero\s+morir\b",
    r"\bno\s+quiero\s+seguir\s+viviendo\b",
    r"\bya\s+no\s+quiero\s+vivir\b",

    r"\bquiero\s+suicidarme\b",
    r"\bvoy\s+a\s+suicidarme\b",
    r"\bpienso\s+suicidarme\b",

    r"\bquiero\s+quitarme\s+la\s+vida\b",
    r"\bvoy\s+a\s+quitarme\s+la\s+vida\b",

    r"\bestoy\s+pensando\s+en\s+suicidarme\b",
    r"\bestoy\s+pensando\s+en\s+el\s+suicidio\b",

    r"\btengo\s+pensamientos\s+suicidas\b",
    r"\btengo\s+ideas\s+suicidas\b",

    r"\bquiero\s+hacerme\s+daño\b",
    r"\bpienso\s+hacerme\s+daño\b",
    r"\bpodría\s+hacerme\s+daño\b",

    r"\btengo\s+un\s+plan\s+para\s+suicidarme\b",

]


# ==================================================
# 2. COMPILE PATTERNS
# ==================================================

COMPILED_PATTERNS = [
    re.compile(
        pattern,
        re.IGNORECASE,
    )
    for pattern in CRISIS_PATTERNS
]


# ==================================================
# 3. CRISIS FALLBACK ASSESSMENT
# ==================================================

def assess_crisis_fallback(
    message: str,
) -> CrisisFallbackResult:
    """
    Detect configured explicit crisis statements.

    Returns:
        CrisisFallbackResult

    A negative result is inconclusive.
    """

    if not isinstance(message, str):

        return CrisisFallbackResult(
            explicit_crisis=False,
            reason="Invalid message input",
            uncertain=True,
        )

    normalized = re.sub(
        r"\s+",
        " ",
        message.strip(),
    )

    if not normalized:

        return CrisisFallbackResult(
            explicit_crisis=False,
            reason="Empty message",
            uncertain=True,
        )

    for pattern in COMPILED_PATTERNS:

        if pattern.search(normalized):

            return CrisisFallbackResult(
                explicit_crisis=True,
                reason="Explicit crisis phrase detected",
                uncertain=True,
            )

    return CrisisFallbackResult(
        explicit_crisis=False,
        reason=(
            "No configured explicit crisis "
            "phrase matched"
        ),
        uncertain=True,
    )


from dataclasses import dataclass
from enum import Enum


class SafetyLevel(str, Enum):
    NORMAL = "normal"
    REVIEW = "review"
    CRISIS = "crisis"


@dataclass(frozen=True)
class SafetyResult:
    level: SafetyLevel
    requires_professional_help: bool
    reason: str


def assess_safety(
    *,
    crisis_detected: bool,
    uncertain: bool = False,
    persistent_distress: bool = False,
    rule_crisis_detected: bool = False,
    assessment_failed: bool = False,
) -> SafetyResult:

    # Highest priority: potential immediate danger.
    if crisis_detected or rule_crisis_detected:
        return SafetyResult(
            level=SafetyLevel.CRISIS,
            requires_professional_help=True,
            reason="Potential immediate safety concern",
        )

    # Assessment unavailable: do not classify as normal.
    if assessment_failed:
        return SafetyResult(
            level=SafetyLevel.REVIEW,
            requires_professional_help=True,
            reason="Safety assessment unavailable",
        )

    if uncertain:
        return SafetyResult(
            level=SafetyLevel.REVIEW,
            requires_professional_help=True,
            reason="Safety concern requires clarification",
        )

    if persistent_distress:
        return SafetyResult(
            level=SafetyLevel.REVIEW,
            requires_professional_help=True,
            reason="Persistent emotional distress",
        )

    return SafetyResult(
        level=SafetyLevel.NORMAL,
        requires_professional_help=False,
        reason="No safety concern detected",
    )

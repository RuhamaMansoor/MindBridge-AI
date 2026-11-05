
"""
MindBridge AI - Medical Safety Regression Tests
Version: 1.1

Run from backend:
    python -m tests.test_medical_regression
"""

from medical_safety_guardian import assess_medical_safety


# Format:
# (name, message, emergency, category, uncertain)

TEST_CASES = [
    (
        "English stroke warning",
        "My face is drooping and my speech is slurred",
        True, "stroke_warning", False,
    ),
    (
        "English sudden vision loss",
        "I suddenly cannot see out of my left eye",
        True, "sudden_vision_loss", False,
    ),
    (
        "Roman Urdu sudden vision loss",
        "Meri baen aankh ki roshni achanak chali gayi hai aur mujhe kuch nazar nahi aa raha",
        True, "sudden_vision_loss", False,
    ),
    (
        "Urdu sudden vision loss",
        "میری بائیں آنکھ کی روشنی اچانک چلی گئی ہے اور مجھے کچھ نظر نہیں آ رہا",
        True, "sudden_vision_loss", False,
    ),
    (
        "English chest pain and breathing difficulty",
        "I have severe chest pain and difficulty breathing",
        True, "cardiorespiratory_emergency", False,
    ),
    (
        "English severe eye pain",
        "I have severe eye pain",
        True, "severe_eye_pain", False,
    ),
    (
        "Hypothetical vision loss",
        "What if someone suddenly loses their vision?",
        False, "sudden_vision_loss", True,
    ),
    (
        "Historical vision loss",
        "Last year I suddenly lost my vision, but now my eyesight is normal",
        False, "sudden_vision_loss", True,
    ),
    (
        "Roman Urdu vision negation",
        "Meri nazar bilkul theek hai, mujhe koi vision loss nahi hai",
        False, "sudden_vision_loss", True,
    ),
    (
        "Breathing difficulty without chest pain",
        "I have no chest pain but I cannot breathe",
        True, "breathing_difficulty", False,
    ),
    (
        "No chest pain but sudden vision loss",
        "I have no chest pain but I suddenly lost my vision",
        True, "sudden_vision_loss", False,
    ),
    (
        "Historical and current vision loss",
        "Last year I lost my vision, but today I suddenly lost my vision again",
        True, "sudden_vision_loss", False,
    ),
    (
        "No slurred speech but facial drooping",
        "I have no slurred speech and my face is suddenly drooping",
        True, "stroke_warning", False,
    ),
    (
        "No facial drooping but slurred speech",
        "My face is normal but my speech is suddenly slurred",
        True, "stroke_warning", False,
    ),
    (
        "No eye pain but sudden vision loss",
        "I have no eye pain but I suddenly cannot see",
        True, "sudden_vision_loss", False,
    ),
    (
        "Roman Urdu stroke warning",
        "Mera chehra achanak terha ho gaya hai aur mujhe bolne mein mushkil ho rahi hai",
        True, "stroke_warning", False,
    ),
    (
        "Roman Urdu severe eye pain",
        "Meri aankh mein bohat tez dard ho raha hai",
        True, "severe_eye_pain", False,
    ),
    (
        "Roman Urdu breathing difficulty",
        "Mujhe saans lene mein bohat mushkil ho rahi hai",
        True, "breathing_difficulty", False,
    ),
    (
        "Roman Urdu sudden vision loss with no pain",
        "Meri aankh mein dard nahi hai lekin achanak nazar chali gayi hai",
        True, "sudden_vision_loss", False,
    ),
    (
        "Urdu stroke warning",
        "میرا چہرہ اچانک ٹیڑھا ہو گیا ہے اور مجھے بولنے میں مشکل ہو رہی ہے",
        True, "stroke_warning", False,
    ),
    (
        "Urdu severe eye pain",
        "میری آنکھ میں بہت شدید درد ہو رہا ہے",
        True, "severe_eye_pain", False,
    ),
    (
        "Urdu breathing difficulty",
        "مجھے سانس لینے میں بہت مشکل ہو رہی ہے",
        True, "breathing_difficulty", False,
    ),
    (
        "Chest pain without breathing difficulty",
        "I have severe chest pain but no breathing difficulty",
        True, "chest_pain", False,
    ),
    (
        "Sudden vision loss with normal speech",
        "My speech is normal but I suddenly cannot see from one eye",
        True, "sudden_vision_loss", False,
    ),
    (
        "Current stroke after historical symptoms",
        "Last year my speech was slurred, but today my face is suddenly drooping",
        True, "stroke_warning", False,
    ),
]


def run_tests():
    passed = 0
    failed = 0
    failures = []

    print("\nMindBridge AI - Medical Safety Regression Tests")
    print("=" * 65)

    for number, case in enumerate(TEST_CASES, start=1):
        (
            name,
            message,
            expected_emergency,
            expected_category,
            expected_uncertain,
        ) = case

        expected = (
            expected_emergency,
            expected_category,
            expected_uncertain,
        )

        try:
            result = assess_medical_safety(message)

            actual = (
                result.emergency_detected,
                result.category,
                result.uncertain,
            )

            if actual == expected:
                passed += 1
                print(f"[PASS] {number:02d} - {name}")

            else:
                failed += 1
                failures.append((number, name, expected, actual))

                print(f"[FAIL] {number:02d} - {name}")
                print(f"       Expected: {expected}")
                print(f"       Actual:   {actual}")
                print(f"       Reason:   {result.reason}")

        except Exception as exc:
            failed += 1
            failures.append(
                (number, name, expected, str(exc))
            )

            print(f"[ERROR] {number:02d} - {name}")
            print(
                f"        {type(exc).__name__}: {exc}"
            )

    print("=" * 65)
    print(f"TOTAL:  {len(TEST_CASES)}")
    print(f"PASSED: {passed}")
    print(f"FAILED: {failed}")

    if failures:
        print("\nFAILED TEST SUMMARY")
        print("-" * 65)

        for number, name, expected, actual in failures:
            print(f"{number:02d}. {name}")
            print(f"    Expected: {expected}")
            print(f"    Actual:   {actual}")

    if failed:
        print("\nREGRESSION TESTS FAILED - REVIEW REQUIRED")
        raise SystemExit(1)

    print("\nALL REGRESSION TESTS PASSED")


if __name__ == "__main__":
    run_tests()

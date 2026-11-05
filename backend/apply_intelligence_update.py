
from pathlib import Path
from datetime import datetime
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
MAIN = ROOT / "main.py"

if not MAIN.exists():
    raise SystemExit("ERROR: main.py not found.")

original = MAIN.read_text(encoding="utf-8-sig")

backup = ROOT / (
    "main_backup_"
    + datetime.now().strftime("%Y%m%d_%H%M%S")
    + ".py"
)
backup.write_text(original, encoding="utf-8")

guidance = '''
    # Practical and intelligent response instructions.
    # Safety routing always takes priority.
    guidance += (
        " RESPONSE INTELLIGENCE AND QUALITY: "
        "Understand the user's actual question and goal. "
        "Use relevant conversation history and constraints. "
        "Do not repeat suggestions the user already tried "
        "and explicitly said did not work. "
        "Give practical, specific and realistic guidance. "
        "When asked for a plan covering a specific number "
        "of days, organize the answer by Day 1, Day 2, "
        "and so on, for exactly that number of days. "
        "Each day should have a concrete action. "
        "When asked for exact words to say to someone, "
        "provide a respectful ready-to-use script. "
        "Respect financial, family and employment "
        "constraints mentioned by the user. "
        "Do not casually recommend resigning from a job "
        "when the user cannot afford to do so. "
        "Explain relevant risks and alternatives. "
        "Do not invent personal circumstances. "
        "Avoid generic reassurance and repetitive advice. "
        "Avoid unnecessary follow-up questions. "
        "Do not guarantee outcomes. "
        "Always prioritize emergency safety guidance, "
        "medical assessment and professional referrals "
        "when appropriate. "
    )

'''

anchor = '    guidance += (\n        " "\n        + LANGUAGE_INSTRUCTIONS.get('

if "RESPONSE INTELLIGENCE AND QUALITY:" in original:
    print("Response intelligence update already exists.")
    sys.exit(0)

if anchor not in original:
    raise SystemExit(
        "ERROR: Expected location not found. "
        "Original main.py was not changed."
    )

updated = original.replace(
    anchor,
    guidance + anchor,
    1
)

compile(updated, str(MAIN), "exec")

try:
    MAIN.write_text(updated, encoding="utf-8")

    print("AI response intelligence updated.")
    print("Running tests...")

    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests", "-q"],
        cwd=ROOT,
        check=False
    )

    if result.returncode != 0:
        MAIN.write_text(original, encoding="utf-8")
        raise SystemExit(
            "Tests failed. Original main.py restored."
        )

    print("SUCCESS: Existing tests passed.")
    print("Backup:", backup.name)

except Exception:
    MAIN.write_text(original, encoding="utf-8")
    raise

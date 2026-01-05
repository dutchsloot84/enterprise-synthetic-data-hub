#!/usr/bin/env python
"""
Lightweight critic checks to keep the demo experience healthy, especially on Windows Git Bash.

Rules:
- Keep execution fast (<10s) and dependency-free.
- Exit non-zero on actionable failures with PASS/FAIL messaging.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAKEFILE = ROOT / "Makefile"
README = ROOT / "README.md"
DEMO_FLOW_DIR = ROOT / "scripts" / "demo_flow"
DEMO_DATA = ROOT / "scripts" / "demo_data.py"


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def check(condition: bool, ok: str, bad: str) -> None:
    if condition:
        print(f"PASS: {ok}")
    else:
        fail(bad)


def main() -> int:
    if not MAKEFILE.is_file():
        fail("Makefile not found")

    makefile_text = MAKEFILE.read_text(encoding="utf-8")
    shell_match = re.search(r"^SHELL\s*:?=\s*(.+)$", makefile_text, re.MULTILINE)
    if not shell_match:
        fail("Makefile SHELL not set")
    shell_value = shell_match.group(1).strip().lower()
    check("bash" in shell_value, f"SHELL uses bash ({shell_value})", f"SHELL is not bash: {shell_value}")

    recipe_lines = [
        line for line in makefile_text.splitlines()
        if line.lstrip().startswith("\t")  # recipe body lines
    ]
    for line in recipe_lines:
        if "python" in line and "$(PYTHON)" not in line:
            fail(f"Recipe line uses raw python instead of $(PYTHON): {line.strip()}")
    print("PASS: Recipes use $(PYTHON) instead of hardcoded python")

    check("which" not in makefile_text, "No use of which in Makefile recipes", "Found 'which' in Makefile")

    if not README.is_file():
        fail("README.md not found for quickstart checks")
    readme = README.read_text(encoding="utf-8").lower()
    check(
        "source .venv/scripts/activate" in readme,
        "README documents Windows Git Bash activation",
        "README missing Windows Git Bash activation command (source .venv/Scripts/activate)",
    )
    check(
        "make demo-gate" in readme,
        "README mentions golden demo command make demo-gate",
        "README missing golden demo command make demo-gate",
    )

    # Optional: run make doctor if available to catch obvious env issues.
    doctor_result = subprocess.run(["make", "doctor"], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if doctor_result.returncode == 0:
        print("PASS: make doctor exited 0")
    else:
        fail("make doctor failed; see output below:\n" + doctor_result.stdout.decode("utf-8", errors="replace"))

    if not DEMO_DATA.exists():
        fail(f"Demo data script missing: {DEMO_DATA}")
    for path in DEMO_FLOW_DIR.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        if "scripts/scripts/demo_data.py" in text:
            fail(f"Found duplicate demo_data path in {path.relative_to(ROOT)}")
    print("PASS: demo flow references demo_data.py without duplicate scripts/ prefix")

    return 0


if __name__ == "__main__":
    sys.exit(main())

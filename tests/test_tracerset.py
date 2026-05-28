import subprocess
import sys
from pathlib import Path
import os
import pytest

ROOT = Path(__file__).resolve().parent.parent

TRACER = ROOT / "tracerset.py"
TESTCASE_DIR = ROOT / "tests" / "program"
LIST_FILE = TESTCASE_DIR / "list.txt"

MODES=[None,"beginner","intermediate","advanced"]

def load_program():
    program = []

    with open(LIST_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            parts = [p.strip() for p in line.split(",")]

            file = TESTCASE_DIR / parts[0]
            expected = parts[1] if len(parts) > 1 else "ok"

            program.append((file, expected))

    return program

@pytest.mark.parametrize("program, expected", load_program())
def test_tracer_runs(program, expected):

    for i in MODES:
        if i is not None:
            result = subprocess.run(
                [sys.executable, str(TRACER), str(i), str(program)],
                capture_output=True,
                input="\n"*1000,
                text=True,
            )
        else:
            result = subprocess.run(
                [sys.executable, str(TRACER),str(program)],
                capture_output=True,
                input="\n"*1000,
                text=True,
            )

        if result.stderr:
            print(result.stderr)
        else:    
            print(result.stdout)

        if expected == "ok":
            assert result.returncode == 0
            assert "Traceback" not in result.stderr
            assert result.stderr == ""
        else:
            stderr_text = result.stderr.lower()

            assert (
                "traceback" in stderr_text
                or "error" in stderr_text
                or "exception" in stderr_text
            )

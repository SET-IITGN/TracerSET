import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

TRACER = ROOT / "tracerset.py"
TESTCASE_DIR = ROOT / "tests" / "program"
LIST_FILE = TESTCASE_DIR / "list.txt"

MODES=["beginner","intermediate","advanced"]

def load_program():
    program = []

    with open(LIST_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue
            program.append(TESTCASE_DIR / line)

    return program


@pytest.mark.parametrize("program", load_program())
def test_tracer_runs(program):

    for i in MODES:
        result = subprocess.run(
            [sys.executable, str(TRACER), str(i), str(program)],
            capture_output=True,
            input="\n"*1000,
            text=True,
        )

        if result.stderr:
            print(result.stderr)
        else:    
            print(result.stdout)

        assert result.returncode == 0
        assert "Traceback" not in result.stdout
        assert result.stderr == ""

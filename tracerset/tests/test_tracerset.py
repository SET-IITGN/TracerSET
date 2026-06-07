import hashlib
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

TRACER = ROOT / "tracerset.py"
TESTCASE_DIR = ROOT / "tests" / "program"

LIST_FILE = TESTCASE_DIR / "list.txt"

MODES = [None, "beginner", "intermediate", "advanced"]

# get all the source files i.e. tracerset.py and utilities/*.py
source_files = [TRACER] + [
    path for path in (ROOT / "utilities").rglob("*.py") if path.is_file()
]
# combine digests from all source files
combined_digest = b""
for source_file in source_files:
    with open(source_file, "rb") as fd:
        combined_digest += hashlib.sha256(fd.read().strip()).digest()
# shorten digest for readability
SHORT_DIGEST = hashlib.md5(combined_digest).hexdigest()

# all output during test execution should go here
# will implement that in future
OUTPUT_DIR = ROOT / "tests" / "outputs"

# OUTPUT_DIR might not exist;
OUTPUT_DIR.mkdir(exist_ok=True)
(OUTPUT_DIR / SHORT_DIGEST).mkdir(exist_ok=True)

print()
print("=" * 64)
print(f"Testing against source version: {SHORT_DIGEST}")
print("=" * 64)
print()


def load_program():
    program = []

    with open(LIST_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            parts = [p.strip() for p in line.split(",")]

            file = TESTCASE_DIR / parts[0]

            # get the hash of test program and compare it with the hash saved at
            # output dir for that test program if it exists
            # This will ensure that tests are always done if the test file is modified
            with open(file, "rb") as fd:
                file_digest = hashlib.sha256(fd.read().strip()).hexdigest()
            digest_file_path = OUTPUT_DIR / SHORT_DIGEST / file.name / "digest.txt"
            if digest_file_path.exists():
                with open(digest_file_path, "r") as fd:
                    if fd.read() == file_digest:
                        continue

            expected = parts[1] if len(parts) > 1 else "ok"

            program.append((file, file_digest, expected))

    return program


@pytest.mark.parametrize("program, program_digest, expected", load_program())
def test_tracer_runs(program, program_digest, expected):

    for i in MODES:
        if i is not None:
            result = subprocess.run(
                [sys.executable, str(TRACER), str(i), str(program)],
                capture_output=True,
                input="\n" * 1000,
                text=True,
            )
        else:
            result = subprocess.run(
                [sys.executable, str(TRACER), str(program)],
                capture_output=True,
                input="\n" * 1000,
                text=True,
            )

        if result.stderr:
            print(result.stderr)
        else:
            print(result.stdout)

        if expected == "ok":
            assert result.returncode == 0
            #assert "Traceback" not in result.stderr
            #assert result.stderr == ""

            # save the digest of test file if tests ran without error
            digest_file_path = OUTPUT_DIR / SHORT_DIGEST / program.name / "digest.txt"
            digest_file_path.parent.mkdir(exist_ok=True)
            with open(digest_file_path, "w") as fd:
                fd.write(program_digest)
        else:
            stderr_text = result.stderr.lower()

            assert (
                "traceback" in stderr_text
                or "error" in stderr_text
                or "exception" in stderr_text
            )

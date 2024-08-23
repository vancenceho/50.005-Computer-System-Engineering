import os
import sys
from difflib import ndiff, context_diff
from pathlib import Path

PY_EXEC = sys.executable
PY_VERSION = sys.version_info
ANSWER_FILE = Path("./answer.txt")

if __name__ == "__main__":
    if PY_VERSION.major < 3 or PY_VERSION.minor < 10:
        raise Exception("Please use Python 3.10 and above. (https://www.python.org/downloads/)")

    if not ANSWER_FILE.exists():
        ANSWER_FILE.touch()
    no_test_files = 6
    banker_file = "banker.py"

    for i in range(no_test_files):
        print(f"\n---TEST {i}---")
        question_file = f"test_files/q{i}.txt"
        expected_answer_file = Path(f"test_files/q{i}_answer.txt")
        command = f"\"{PY_EXEC}\" {banker_file} {question_file} > {ANSWER_FILE}"
        os.system(command)

        with ANSWER_FILE.open('r') as ans_fp:
            with expected_answer_file.open('r') as exp_fp:
                answers = ans_fp.readlines()
                expected_answers = exp_fp.readlines()

                difference = list(ndiff(answers, expected_answers))
                cont_diff = list(context_diff(answers, expected_answers, n=0))
                if len(cont_diff) == 0:
                    print(f"PASSED TEST {i}")
                else:
                    print(f"FAILED TEST {i} (+ indicates an expected line, - indicates an unexpected line):")
                    print("".join(difference))

    # Delete the generated answer file
    ANSWER_FILE.unlink(missing_ok=True)

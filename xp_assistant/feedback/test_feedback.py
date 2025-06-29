from __future__ import annotations

import subprocess

from xp_assistant.feedback.feedback import FeedbackMechanism, Ok, NotOk, InputDescription


class TestFeedback(FeedbackMechanism):
    def __init__(
        self,
        directory: str,
        test_file: str
    ):
        self._directory = directory
        self._test_file = test_file

    def get_constraint(self) -> str:
        with open(f'{self._directory}/{self._test_file}') as f:
            test_code = f.read()

        return 'It needs to pass these tests: \n\n' + test_code

    def get_feedback(self) -> Ok | NotOk:
        result = subprocess.run(
            ["python", "-m", "unittest", self._test_file],
            cwd=self._directory,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return Ok()

        return NotOk(f"Test failed:\n{result.stdout}\n{result.stderr}")

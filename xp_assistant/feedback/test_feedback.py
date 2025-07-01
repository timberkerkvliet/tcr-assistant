from __future__ import annotations

import subprocess

from xp_assistant.source_code import SourceCodeFile
from xp_assistant.feedback.feedback import FeedbackMechanism, Ok, NotOk, InputDescription


class TestFeedback(FeedbackMechanism):
    def __init__(
        self,
        test_file: SourceCodeFile
    ):
        self._test_file = test_file

    def get_description(self) -> str:
        return 'Running tests'

    def get_constraint(self) -> str:
        return 'It needs to pass these tests: \n\n' + self._test_file.read_code()

    def get_feedback(self) -> Ok | NotOk:
        result = subprocess.run(
            ["python", "-m", "unittest", self._test_file.file_path],
            cwd=self._test_file.project_path,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return Ok(description='Tests passed')

        return NotOk(f"Test failed:\n{result.stdout}\n{result.stderr}")

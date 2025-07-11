from __future__ import annotations

import subprocess
from logging import Logger

from tcr_assistant.source_code import SourceCodeFile
from tcr_assistant.feedback.feedback import FeedbackMechanism, Accepted, NotAccepted


class TestFeedback(FeedbackMechanism):
    def __init__(
        self,
        test_file: SourceCodeFile,
        logger: Logger
    ):
        self._test_file = test_file
        self._logger = logger

    def get_feedback(self) -> Accepted | NotAccepted:
        result = subprocess.run(
            ["python", "-m", "unittest", self._test_file.file_path],
            cwd=self._test_file.project_path,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            self._logger.info('Tests passed')
            return Accepted(description='Tests passed')

        self._logger.info('Tests failed')
        return NotAccepted(f"Test failed:\n{result.stdout}\n{result.stderr}")

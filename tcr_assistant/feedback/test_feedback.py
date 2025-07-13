from __future__ import annotations

import subprocess
from logging import Logger

from build.lib.tcr_assistant.source_code import SourceCodePair
from tcr_assistant.source_code import SourceCodeFile
from tcr_assistant.feedback.feedback import FeedbackMechanism, Accepted, NotAccepted


class TestFeedback(FeedbackMechanism):
    def __init__(
        self,
        pair: SourceCodePair,
        logger: Logger
    ):
        self._test_file = pair.test_code
        self._prod_file = pair.production_code
        self._logger = logger

    def get_feedback(self) -> Accepted | NotAccepted:
        result = subprocess.run(
            ['coverage', 'run', '-m', 'unittest', self._test_file.file_path],
            cwd=self._test_file.project_path,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            self._logger.info('Tests failed')
            return NotAccepted(f"Test failed:\n{result.stdout}\n{result.stderr}")
        coverage = subprocess.run(
            ['coverage', 'report', self._prod_file.file_path],
            cwd=self._test_file.project_path,
            capture_output=True,
            text=True
        ).stdout.split('%')[0].split(' ')[-1]
        self._logger.info(f'Tests passed with {coverage}% coverage')
        return Accepted(description='Tests passed')



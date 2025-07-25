from logging import Logger

import dspy

from tcr_assistant.source_code import SourceCodeFile
from tcr_assistant.feedback.feedback import FeedbackMechanism
from tcr_assistant.code_generator.signature import ChangeExistingCode

MAX_ATTEMPTS = 3

class ChangeCodeIterator:
    def __init__(
        self,
        feedback: FeedbackMechanism,
        target: SourceCodeFile,
        main_goal: str,
        logger: Logger
    ):
        self._feedback = feedback
        self._target = target
        self._main_goal = main_goal
        self._logger = logger

    def run(self) -> bool:
        feedback: str = ''

        for _ in range(MAX_ATTEMPTS):
            code_generator = dspy.Predict(ChangeExistingCode)

            self._logger.info('Generating code...')
            res = code_generator(
                current_code=self._target.read_code(),
                main_goal=self._main_goal,
                constraints=self._feedback.get_constraint() + feedback
            )
            self._logger.info('Code generated')

            self._target.write_code(res.python_code)

            res = self._feedback.get_feedback()

            if res.is_ok():
                return True

            feedback = res.explanation

        return False

from dataclasses import dataclass
from typing import Callable

from tcr_assistant.code_generator.context import Context
from tcr_assistant.feedback.feedback import FeedbackMechanism
from tcr_assistant.source_code import SourceCodePair, SourceCodeFile

@dataclass
class FailedAttempt(Context):
    why: str


class FeedbackLoop:
    def __init__(self, max_attempts: int):
        self._max_attempts = max_attempts

    def run(
        self,
        target: SourceCodeFile,
        code_generator: Callable[[list[Context]], str],
        feedback_mechanism: FeedbackMechanism
    ):
        context = []

        for _ in range(self._max_attempts):
            generated_code = code_generator(context)
            target.write_code(generated_code)
            feedback_result = feedback_mechanism.get_feedback()

            if feedback_result.is_ok():
                return

            context = [FailedAttempt(feedback_result.explanation)]

        raise NotImplementedError

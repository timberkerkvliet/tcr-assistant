from dataclasses import dataclass
from typing import Callable

from tcr_assistant.code_generator.context import ContextElement, Context
from tcr_assistant.code_generator.context_elements.failed_attempt import FailedAttempt
from tcr_assistant.feedback.feedback import FeedbackMechanism
from tcr_assistant.source_code import SourceCodeFile


class FeedbackLoop:
    def __init__(self, max_attempts: int):
        self._max_attempts = max_attempts

    def run(
        self,
        target: SourceCodeFile,
        code_generator: Callable[[Context], str],
        feedback_mechanism: FeedbackMechanism,
        context: Context
    ):
        additional_elements: list[ContextElement] = []
        for _ in range(self._max_attempts):
            generated_code = code_generator(context.add_elements(additional_elements))
            target.write_code(generated_code)
            feedback_result = feedback_mechanism.get_feedback()

            if feedback_result.is_ok():
                return

            additional_elements = [FailedAttempt(feedback_result.explanation)]

        raise NotImplementedError

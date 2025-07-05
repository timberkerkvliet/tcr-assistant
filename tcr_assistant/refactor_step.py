from logging import Logger

from tcr_assistant.change_code_iterator import ChangeCodeIterator
from tcr_assistant.feedback.feedback_chain import FeedbackChain
from tcr_assistant.feedback.manual_feedback import ManualFeedback
from tcr_assistant.feedback.test_feedback import TestFeedback
from tcr_assistant.source_code import SourceCodePair
from tcr_assistant.version_control.version_control import VersionControl


class RefactorStep:
    def __init__(self, version_control: VersionControl, logger: Logger):
        self._version_control = version_control
        self._logger = logger

    def run(self, source_code_pair: SourceCodePair):
        refactor_hint = input("Refactor hint: ")

        feedback = FeedbackChain(
            [
                TestFeedback(source_code_pair.test_code, self._logger),
                ManualFeedback()
            ]
        )

        iterator = ChangeCodeIterator(
            feedback=feedback,
            target=source_code_pair.production_code,
            main_goal=f'Refactor with hint: {refactor_hint}',
            logger=self._logger
        )

        if iterator.run():
            self._version_control.commit(source_code_pair.production_code)
        else:
            self._version_control.revert(source_code_pair.production_code)

from logging import Logger

from xp_assistant.change_code_iterator import ChangeCodeIterator
from xp_assistant.feedback.feedback_chain import FeedbackChain
from xp_assistant.feedback.manual_feedback import ManualFeedback
from xp_assistant.feedback.test_feedback import TestFeedback
from xp_assistant.source_code import SourceCodePair
from xp_assistant.version_control.version_control import VersionControl


class AddBehaviorStep:
    def __init__(self, version_control: VersionControl, logger: Logger):
        self._version_control = version_control
        self._logger = logger

    def run(self, source_code_pair: SourceCodePair):
        test_description = input("Describe new test: ")

        feedback = FeedbackChain(
            [
                ManualFeedback()
            ]
        )

        iterator = ChangeCodeIterator(
            feedback=feedback,
            target=source_code_pair.test_code,
            main_goal=f'Add a new test and return the whole file: {test_description}',
            logger=self._logger
        )

        if not iterator.run():
            raise NotImplementedError

        feedback = FeedbackChain(
            [
                TestFeedback(source_code_pair.test_code, self._logger)
            ]
        )

        iterator = ChangeCodeIterator(
            feedback=feedback,
            target=source_code_pair.production_code,
            main_goal=f'Make all - including the new - test pass with minimal changes',
            logger=self._logger
        )

        if iterator.run():
            self._version_control.commit(source_code_pair.production_code)
        else:
            self._version_control.revert(source_code_pair.production_code)

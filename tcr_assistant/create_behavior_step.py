from logging import Logger

from tcr_assistant.create_code_iterator import CreateCodeIterator
from tcr_assistant.feedback.feedback_chain import FeedbackChain
from tcr_assistant.feedback.manual_feedback import ManualFeedback
from tcr_assistant.feedback.test_feedback import TestFeedback
from tcr_assistant.source_code import SourceCodePair
from tcr_assistant.version_control.version_control import VersionControl


class CreateBehaviorStep:
    def __init__(self, version_control: VersionControl, logger: Logger):
        self._version_control = version_control
        self._logger = logger

    def run(self, source_code_pair: SourceCodePair):
        test_description = input("Describe first test: ")

        feedback = FeedbackChain(
            [
                ManualFeedback()
            ]
        )

        iterator = CreateCodeIterator(
            feedback=feedback,
            target=source_code_pair.test_code,
            main_goal=f'Create a python UnitTest class. Dont add a __main__ section. You can import production code with: from .{source_code_pair.production_code.name()} import ... . This describes the first test: {test_description}',
            logger=self._logger
        )

        if not iterator.run():
            self._version_control.revert(source_code_pair.production_code)
            self._logger.warning('Step failed')
            return

        feedback = FeedbackChain(
            [
                TestFeedback(source_code_pair.test_code, self._logger)
            ]
        )

        iterator = CreateCodeIterator(
            feedback=feedback,
            target=source_code_pair.production_code,
            main_goal=f'Create a python module that passes the test and ONLY passes this test. Imagine you are a senior python XP engineer',
            logger=self._logger
        )

        if iterator.run():
            self._version_control.commit(source_code_pair.production_code)
        else:
            self._version_control.revert(source_code_pair.production_code)

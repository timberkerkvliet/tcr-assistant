from xp_assistant.change_code_iterator import ChangeCodeIterator
from xp_assistant.feedback.feedback_chain import FeedbackChain
from xp_assistant.feedback.manual_feedback import ManualFeedback
from xp_assistant.feedback.print_feedback import PrintFeedback
from xp_assistant.feedback.test_feedback import TestFeedback
from xp_assistant.source_code import SourceCodePair
from xp_assistant.version_control.version_control import VersionControl


class RefactorStep:
    def __init__(self, version_control: VersionControl):
        self._version_control = version_control

    def run(self, source_code_pair: SourceCodePair):
        refactor_hint = input("Refactor hint: ")

        feedback = FeedbackChain(
            [
                PrintFeedback(TestFeedback(source_code_pair.test_code)),
                PrintFeedback(ManualFeedback())
            ]
        )

        iterator = ChangeCodeIterator(
            feedback=feedback,
            target=source_code_pair.production_code,
            main_goal=f'Refactor with hint: {refactor_hint}'
        )

        if iterator.run():
            self._version_control.commit(source_code_pair.production_code)
        else:
            self._version_control.revert(source_code_pair.production_code)

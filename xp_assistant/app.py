import os

import dspy

from xp_assistant.feedback.feedback_chain import FeedbackChain
from xp_assistant.feedback.manual_feedback import ManualFeedback
from xp_assistant.feedback.print_feedback import PrintFeedback
from xp_assistant.feedback.test_feedback import TestFeedback
from xp_assistant.signature import ChangeExistingCode
from xp_assistant.version_control.commit import CommitChanges, GitCommit, CommitPrintLine
from xp_assistant.version_control.revert import RevertChanges, GitRevert
from xp_assistant.version_control.revert import RevertPrintLine


class App:
    def __init__(
        self,
        commit_changes: CommitChanges,
        revert_changes: RevertChanges
    ):
        self._commit_changes = commit_changes
        self._revert_changes = revert_changes

    def run(self):
        while True:
            refactor_hint = input("Refactor hint: ")
            with open(f'{PROJECT_DIR}/{PROD_FILE}') as f:
                prod_code = f.read()

            code_generator = dspy.Predict(ChangeExistingCode)

            feedback = FeedbackChain(
                [
                    PrintFeedback(TestFeedback(PROJECT_DIR, TEST_FILE)),
                    PrintFeedback(ManualFeedback())
                ]
            )

            res = code_generator(
                current_code=prod_code,
                main_goal=f'Refactor with hint: {refactor_hint}',
                constraints=feedback.get_constraint()
            )

            with open(f'{PROJECT_DIR}/{PROD_FILE}', 'wb') as f:
                f.write(res.python_code.encode())

            res = feedback.get_feedback()

            if res.is_ok():
                self._commit_changes.commit()
            else:
                print("❌ Reverting changes...")
                self._revert_changes.revert()


api_key = os.environ["OPENAI_KEY"]
gemini = dspy.LM(model='openai/gpt-4o-mini', api_key=api_key)
dspy.configure(lm=gemini)



PROJECT_DIR = '/Users/timberkerkvliet/PycharmProjects/fibonacci'
TEST_FILE = 'fibonacci/test_fibonacci.py'
PROD_FILE = 'fibonacci/fibo.py'

commit_changes = CommitPrintLine(GitCommit(PROJECT_DIR))
revert_changes = RevertPrintLine(GitRevert(PROJECT_DIR))

app = App(commit_changes, revert_changes)

app.run()

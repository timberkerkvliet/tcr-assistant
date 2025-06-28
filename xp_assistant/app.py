import os

import dspy

from xp_assistant.version_control.revert import RevertPrintLine
from xp_assistant.version_control.revert import RevertChanges, GitRevert
from xp_assistant.version_control.commit import CommitChanges, GitCommit, CommitPrintLine
from xp_assistant.signature import RefactorSignature

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
            with open(f'{PROJECT_DIR}/{TEST_FILE}') as f:
                test_code = f.read()

            with open(f'{PROJECT_DIR}/{PROD_FILE}') as f:
                prod_code = f.read()

            res = code_generator(test_code=test_code, prod_code=prod_code, refactor_hint=refactor_hint)

            with open(f'{PROJECT_DIR}/{PROD_FILE}', 'wb') as f:
                f.write(res.python_code.encode())

            exit_code = os.system(f"cd {PROJECT_DIR} && python -m unittest {TEST_FILE}")

            if exit_code == 0:
                print("✅ Tests passed.\n")

                # Ask for approval
                approve = input("\nDo you want to commit these changes? (y/n): ").strip().lower()
                if approve == "y":
                    self._commit_changes.commit()
                else:
                    self._revert_changes.revert()
                    print("❌ Changes reverted.")
            else:
                print("❌ Tests failed. Reverting changes...")
                self._revert_changes.revert()


api_key = os.environ["OPENAI_KEY"]
gemini = dspy.LM(model='openai/gpt-4o-mini', api_key=api_key)
dspy.configure(lm=gemini)

code_generator = dspy.Predict(RefactorSignature)

PROJECT_DIR = '/Users/timberkerkvliet/PycharmProjects/fibonacci'
TEST_FILE = 'fibonacci/test_fibonacci.py'
PROD_FILE = 'fibonacci/fibo.py'

commit_changes = CommitPrintLine(GitCommit(PROJECT_DIR))
revert_changes = RevertPrintLine(GitRevert(PROJECT_DIR))

app = App(commit_changes, revert_changes)

app.run()

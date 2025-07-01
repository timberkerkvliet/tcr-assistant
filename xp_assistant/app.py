import os

import dspy

from xp_assistant.refactor_step import RefactorStep
from xp_assistant.source_code import SourceCodePair, SourceCodeFile
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
            RefactorStep(
                self._commit_changes,
                self._revert_changes
            ).run(
                SourceCodePair(
                    production_code=SourceCodeFile(
                        project_path=PROJECT_DIR,
                        file_path=PROD_FILE
                    ),
                    test_code=SourceCodeFile(
                        project_path=PROJECT_DIR,
                        file_path=TEST_FILE
                    )
                )
            )


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

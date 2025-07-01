import os
from logging import Logger

import dspy

from xp_assistant.add_behavior_step import AddBehaviorStep
from xp_assistant.refactor_step import RefactorStep
from xp_assistant.source_code import SourceCodePair, SourceCodeFile
from xp_assistant.version_control.git_version_control import GitVersionControl
from xp_assistant.version_control.version_control import VersionControl


class App:
    def __init__(
        self,
        version_control: VersionControl,
        logger: Logger
    ):
        self._version_control = version_control
        self._logger = logger

    def run(self, source_code_pair: SourceCodePair):
        while True:
            AddBehaviorStep(self._version_control, self._logger).run(source_code_pair)
            RefactorStep(
                self._version_control,
                self._logger
            ).run(source_code_pair)


api_key = os.environ["OPENAI_KEY"]
gemini = dspy.LM(model='openai/gpt-4o-mini', api_key=api_key)
dspy.configure(lm=gemini)


PROJECT_DIR = '/Users/timberkerkvliet/PycharmProjects/fibonacci'
TEST_FILE = 'fibonacci/test_fibonacci.py'
PROD_FILE = 'fibonacci/fibo.py'

logger = Logger('default')

app = App(GitVersionControl(logger), logger)

app.run(SourceCodePair(
    production_code=SourceCodeFile(PROJECT_DIR, PROD_FILE),
    test_code=SourceCodeFile(PROJECT_DIR, TEST_FILE)
))

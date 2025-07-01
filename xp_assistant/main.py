import os
from logging import Logger

import dspy

from xp_assistant.app import App
from xp_assistant.source_code import SourceCodePair, SourceCodeFile
from xp_assistant.version_control.git_version_control import GitVersionControl

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

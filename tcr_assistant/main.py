import argparse

import yaml
from logging import Logger, StreamHandler
from pathlib import Path

import dspy

from tcr_assistant.add_behavior_step import AddBehaviorStep
from tcr_assistant.app import App
from tcr_assistant.code_generator.context import Context
from tcr_assistant.code_generator.dspy_code_generator import DsPyTestCodeCodeGenerator, DsPyImplementationCodeGenerator
from tcr_assistant.feedback_loop import FeedbackLoop
from tcr_assistant.source_code import SourceCodePair, SourceCodeFile
from tcr_assistant.version_control.git_version_control import GitVersionControl

with open("xp-assistant.yml", "r") as f:
    config = yaml.safe_load(f)

llm = dspy.LM(model=config['llm']['model'], api_key=config['llm']['api_key'])
dspy.configure(lm=llm)

PROJECT_DIR = str(Path.cwd())
parser = argparse.ArgumentParser(description="Run XP Assistant")
parser.add_argument("file", help="Path to the production source file, relative to project root.")
parser.add_argument("--test_file", help="Path to the test file, relative to project root.")
args = parser.parse_args()

logger = Logger('default')
logger.addHandler(StreamHandler())

def test_from_prod_file(file: str) -> str:
    parts = file.split('/')
    parts[-1] = 'test_' + parts[-1]

    return '/'.join(parts)


source_code_pair = SourceCodePair(
    production_code=SourceCodeFile(PROJECT_DIR, args.file),
    test_code=SourceCodeFile(PROJECT_DIR, args.test_file or test_from_prod_file(args.file))
)

version_control = GitVersionControl(logger)

def context_mapper(context: Context) -> str:
    return ''

app = App(
    version_control,
    logger,
    AddBehaviorStep(
        version_control,
        logger,
        DsPyTestCodeCodeGenerator(context_mapper),
        DsPyImplementationCodeGenerator(context_mapper),
        FeedbackLoop(3)
    )
)

app.run(source_code_pair)

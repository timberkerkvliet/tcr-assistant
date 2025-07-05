import argparse

import yaml
from logging import Logger, StreamHandler
from pathlib import Path

import dspy

from tcr_assistant.app import App
from tcr_assistant.source_code import SourceCodePair, SourceCodeFile
from tcr_assistant.version_control.git_version_control import GitVersionControl

# Load config from YAML
with open("xp-assistant.yml", "r") as f:
    config = yaml.safe_load(f)

# Set up LLM with config values
llm = dspy.LM(model=config['llm']['model'], api_key=config['llm']['api_key'])
dspy.configure(lm=llm)

# Project paths
PROJECT_DIR = str(Path.cwd())
parser = argparse.ArgumentParser(description="Run XP Assistant")
parser.add_argument("file", help="Path to the production source file, relative to project root.")
parser.add_argument("--test_file", help="Path to the test file, relative to project root.")
args = parser.parse_args()

# Logging
logger = Logger('default')
logger.addHandler(StreamHandler())

def test_from_prod_file(file: str) -> str:
    parts = file.split('/')
    parts[-1] = 'test_' + parts[-1]

    return '/'.join(parts)

# App setup and run
app = App(GitVersionControl(logger), logger)
app.run(SourceCodePair(
    production_code=SourceCodeFile(PROJECT_DIR, args.file),
    test_code=SourceCodeFile(PROJECT_DIR, args.test_file or test_from_prod_file(args.file))
))

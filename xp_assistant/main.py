import yaml
from logging import Logger, StreamHandler
from pathlib import Path

import dspy

from xp_assistant.app import App
from xp_assistant.source_code import SourceCodePair, SourceCodeFile
from xp_assistant.version_control.git_version_control import GitVersionControl

# Load config from YAML
with open("xp-assistant.yml", "r") as f:
    config = yaml.safe_load(f)

# Set up LLM with config values
llm = dspy.LM(model=config['llm']['model'], api_key=config['llm']['api_key'])
dspy.configure(lm=llm)

# Project paths
PROJECT_DIR = str(Path.cwd())
TEST_FILE = config["test_file"]
PROD_FILE = config["prod_file"]

# Logging
logger = Logger('default')
logger.addHandler(StreamHandler())

# App setup and run
app = App(GitVersionControl(logger), logger)
app.run(SourceCodePair(
    production_code=SourceCodeFile(PROJECT_DIR, PROD_FILE),
    test_code=SourceCodeFile(PROJECT_DIR, TEST_FILE)
))

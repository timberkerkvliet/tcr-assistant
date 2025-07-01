import yaml
from logging import Logger, StreamHandler
from pathlib import Path

import dspy

from xp_assistant.app import App
from xp_assistant.source_code import SourceCodePair, SourceCodeFile
from xp_assistant.version_control.git_version_control import GitVersionControl

# Load config from YAML
with open("xp-assistant.yaml", "r") as f:
    config = yaml.safe_load(f)

# Set up LLM with config values
gemini = dspy.LM(model=config["model"], api_key=config["model_api_key"])
dspy.configure(lm=gemini)

# Project paths
PROJECT_DIR = config["project_dir"]
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

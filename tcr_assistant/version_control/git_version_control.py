import subprocess
from logging import Logger

from tcr_assistant.source_code import SourceCodeFile
from tcr_assistant.version_control.version_control import VersionControl


class GitVersionControl(VersionControl):
    def __init__(self, logger: Logger):
        self._logger = logger

    def commit(self, source_code_file: SourceCodeFile):
        subprocess.run(
            ['git', 'add', source_code_file.file_path],
            cwd=source_code_file.project_path,
            capture_output=True,
            text=True
        )
        subprocess.run(
            ['git', 'commit', '-m', 'TCR commit', source_code_file.file_path],
            cwd=source_code_file.project_path,
            capture_output=True,
            text=True
        )
        self._logger.info(f'Changes to {source_code_file.file_path} commited')

    def revert(self, source_code_file: SourceCodeFile):
        subprocess.run(
            ['git', 'checkout', source_code_file.file_path],
            cwd=source_code_file.project_path,
            capture_output=True,
            text=True
        )
        self._logger.info(f'Changes to {source_code_file.file_path} reverted')

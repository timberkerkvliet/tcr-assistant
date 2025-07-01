from abc import ABC, abstractmethod

from xp_assistant.source_code import SourceCodeFile


class VersionControl(ABC):
    @abstractmethod
    def commit(self, source_file: SourceCodeFile):
        """Commit"""

    @abstractmethod
    def revert(self, source_file: SourceCodeFile):
        """Revert"""

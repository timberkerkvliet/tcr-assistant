import os
from abc import ABC, abstractmethod


class RevertChanges(ABC):
    @abstractmethod
    def revert(self):
        ...


class RevertPrintLine(RevertChanges):
    def __init__(self, commit_changes: RevertChanges):
        self.commit_changes = commit_changes

    def revert(self):
        self.commit_changes.revert()
        print("Changes reverted.")


class GitRevert(RevertChanges):
    def __init__(self, directory: str):
        self.directory = directory

    def revert(self):
        os.system(f"cd {self.directory} && git reset --hard")

import os
from abc import ABC, abstractmethod


class CommitChanges(ABC):
    @abstractmethod
    def commit(self):
        ...


class CommitPrintLine(CommitChanges):
    def __init__(self, commit_changes: CommitChanges):
        self.commit_changes = commit_changes

    def commit(self):
        self.commit_changes.commit()
        print("✅ Changes committed.")


class GitCommit(CommitChanges):
    def __init__(self, directory: str):
        self.directory = directory

    def commit(self):
        os.system(f'cd {self.directory} && git commit -am "Passing tests"')

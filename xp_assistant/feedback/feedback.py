from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from dspy import InputField


@dataclass(frozen=True)
class InputDescription:
    field: InputField
    field_name: str


@dataclass(frozen=True)
class Ok:
    @staticmethod
    def is_ok() -> bool:
        return True

@dataclass(frozen=True)
class NotOk:
    why: str

    @staticmethod
    def is_ok() -> bool:
        return False



class FeedbackMechanism(ABC):
    @abstractmethod
    def get_constraint(self) -> str:
        """Get all sorts of feedback on code"""

    @abstractmethod
    def get_feedback(self) -> Ok | NotOk:
        """Get all sorts of feedback on code"""

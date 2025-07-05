from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from dspy import InputField


@dataclass(frozen=True)
class InputDescription:
    field: InputField
    field_name: str


@dataclass(frozen=True)
class Accepted:
    description: str

    @staticmethod
    def is_ok() -> bool:
        return True

@dataclass(frozen=True)
class NotAccepted:
    explanation: str

    @staticmethod
    def is_ok() -> bool:
        return False



class FeedbackMechanism(ABC):
    @abstractmethod
    def get_feedback(self) -> Accepted | NotAccepted:
        """Get all sorts of feedback on code"""

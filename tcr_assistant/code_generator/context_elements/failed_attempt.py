from dataclasses import dataclass

from tcr_assistant.code_generator.context_element import ContextElement


@dataclass
class FailedAttempt(ContextElement):
    why: str


def map_failed_attempt(element: FailedAttempt) -> str:
    return ''

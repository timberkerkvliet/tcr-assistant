from dataclasses import dataclass

from tcr_assistant.code_generator.context_element import ContextElement


@dataclass
class Tests(ContextElement):
    test_code: str


def map_test_code(context_element: Tests) -> str:
    return f'These are the tests: {context_element.test_code}'

from typing import Optional, Callable

import dspy
from tcr_assistant.code_generator.code_generator import TestCodeGenerator, ImplementationCodeGenerator
from tcr_assistant.code_generator.context import Context
from tcr_assistant.code_generator.signature import ChangeExistingCode, CreateNewCode


class DsPyTestCodeCodeGenerator(TestCodeGenerator):
    def __init__(self, context_mapper: Callable[[Context], str]):
        self._context_mapper = context_mapper

    def add_tests(self, new_tests_description: str, context: list[Context],
                  existing_test_code: Optional[str] = None) -> str:


        if existing_test_code is not None:
            code_generator = dspy.Predict(ChangeExistingCode)

            return code_generator(
                existing_code=existing_test_code,
                main_goal=f'Add these test(s): {new_tests_description}',
                constraints=[self._context_mapper(piece) for piece in context]
            ).python_code

        code_generator = dspy.Predict(CreateNewCode)

        return code_generator(
            main_goal=f'Create a test file. This describes the first test(s): {new_tests_description}',
            constraints=[self._context_mapper(piece) for piece in context]
        ).python_code



class DsPyImplementationCodeGenerator(ImplementationCodeGenerator):
    def __init__(self, context_mapper: Callable[[Context], str]):
        self._context_mapper = context_mapper

    def implement(self, test_code: str, context: list[Context], existing_production_code: Optional[str] = None) -> str:
        if existing_production_code is not None:
            code_generator = dspy.Predict(ChangeExistingCode)

            return code_generator(
                existing_code=existing_production_code,
                main_goal=f'Make sure all these test pass: {test_code}',
                constraints=[self._context_mapper(piece) for piece in context]
            ).python_code

        code_generator = dspy.Predict(CreateNewCode)

        return code_generator(
            main_goal=f'Create a python file. Make sure all these test pass:: {test_code}',
            constraints=[self._context_mapper(piece) for piece in context]
        ).python_code

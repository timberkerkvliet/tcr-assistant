from typing import Optional, Callable

import dspy
from tcr_assistant.code_generator.code_generator import TestCodeGenerator, ImplementationCodeGenerator
from tcr_assistant.code_generator.context import ContextElement, Context, ContextMapper

from tcr_assistant.code_generator.context_elements.create_new_test_file import CreateNewTestFile
from tcr_assistant.code_generator.context_elements.tests import Tests
from tcr_assistant.code_generator.signature import ChangeExistingCode, CreateNewCode


class DsPyTestCodeCodeGenerator(TestCodeGenerator):
    def __init__(self, context_mapper: ContextMapper):
        self._context_mapper = context_mapper

    def add_tests(
        self,
        new_tests_description: str,
        context: Context,
        existing_test_code: Optional[str] = None
    ) -> str:
        if existing_test_code is not None:
            code_generator = dspy.Predict(ChangeExistingCode)

            return code_generator(
                current_code=existing_test_code,
                main_goal=f'Add these test(s) the the file and return all test code: {new_tests_description}',
                constraints=context.map(self._context_mapper)
            ).python_code

        code_generator = dspy.Predict(CreateNewCode)

        return code_generator(
            main_goal=f'Create a test file. This describes the first test(s): {new_tests_description}',
            constraints=context.map(self._context_mapper)
        ).python_code



class DsPyImplementationCodeGenerator(ImplementationCodeGenerator):
    def __init__(self, context_mapper: ContextMapper):
        self._context_mapper = context_mapper

    def implement(
        self,
        test_code: str,
        context: Context,
        existing_production_code: Optional[str] = None
    ) -> str:
        if existing_production_code is not None:
            code_generator = dspy.Predict(ChangeExistingCode)

            return code_generator(
                current_code=existing_production_code,
                main_goal=f'Make changes to make sure all tests pass. Make the change as small as possible. Do not create more code than necessary. Ensure that all code is covered by the tests.',
                constraints=context
                    .add_element(Tests(test_code))
                    .map(self._context_mapper)
            ).python_code

        code_generator = dspy.Predict(CreateNewCode)

        return code_generator(
            main_goal=f'Create a python file that make all these test pass. Make the file as small as possible. Do not create more code than necessary. Ensure that all code is covered by the tests.',
            constraints=context
                .add_element(Tests(test_code))
                .map(self._context_mapper)
        ).python_code

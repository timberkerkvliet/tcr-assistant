from logging import Logger

from tcr_assistant.code_generator.code_generator import TestCodeGenerator, ImplementationCodeGenerator
from tcr_assistant.code_generator.context import Context
from tcr_assistant.code_generator.context_elements.create_new_test_file import CreateNewTestFile
from tcr_assistant.feedback.manual_feedback import ManualFeedback
from tcr_assistant.feedback.test_feedback import TestFeedback
from tcr_assistant.feedback_loop import FeedbackLoop
from tcr_assistant.source_code import SourceCodePair
from tcr_assistant.version_control.version_control import VersionControl


class AddBehaviorStep:
    def __init__(
        self,
        version_control: VersionControl,
        logger: Logger,
        test_code_generator: TestCodeGenerator,
        implementation_code_generator: ImplementationCodeGenerator,
        feedback_loop: FeedbackLoop
    ):
        self._version_control = version_control
        self._logger = logger
        self._test_code_generator = test_code_generator
        self._implementation_code_generator = implementation_code_generator
        self._feedback_loop = feedback_loop

    def run(self, source_code_pair: SourceCodePair):
        test_description = input("Describe new test(s): ")
        existing_test_code = source_code_pair.test_code.read_code()
        existing_production_code = source_code_pair.production_code.read_code()

        self._feedback_loop.run(
            target=source_code_pair.test_code,
            code_generator=lambda context: self._test_code_generator.add_tests(
                new_tests_description=test_description,
                existing_test_code=existing_test_code,
                context=context
            ),
            feedback_mechanism=ManualFeedback(),
            context=Context.with_element(CreateNewTestFile(source_code_pair.production_code)) if source_code_pair.test_code.is_empty() else Context.empty()
        )

        self._feedback_loop.run(
            target=source_code_pair.production_code,
            code_generator=lambda context: self._implementation_code_generator.implement(
                test_code=source_code_pair.test_code.read_code(),
                existing_production_code=existing_production_code,
                context=context
            ),
            feedback_mechanism=TestFeedback(source_code_pair.test_code, self._logger),
            context=Context.empty()
        )

        self._version_control.commit(source_code_pair.test_code)
        self._version_control.commit(source_code_pair.production_code)

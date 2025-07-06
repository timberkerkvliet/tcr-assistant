from enum import Enum

from tcr_assistant.code_generator.code_generator import ContextElement


class PythonTestFramework(ContextElement, Enum):
    UNITTEST = 0
    PYTEST = 1




def framework_formatter(context: PythonTestFramework) -> str:
    if context == context.UNITTEST:
        return 'Use the standard UnitTest class. Dont add a __main__ section.'

    raise NotImplementedError

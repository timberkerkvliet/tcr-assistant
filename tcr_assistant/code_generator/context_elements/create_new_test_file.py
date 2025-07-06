from dataclasses import dataclass

from tcr_assistant.code_generator.context_element import ContextElement
from tcr_assistant.source_code import SourceCodeFile


@dataclass
class CreateNewTestFile(ContextElement):
    production_file: SourceCodeFile


def map_how_to_create_new_test_file_unittest(element: CreateNewTestFile) -> str:
    return f'Use the standard UnitTest class. Dont add a __main__ section. Import production code with: `from .{element.production_file.name()} import ...`'

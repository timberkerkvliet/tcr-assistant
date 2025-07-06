from abc import ABC, abstractmethod
from typing import Optional

from tcr_assistant.code_generator.context import Context


class TestCodeGenerator(ABC):
    @abstractmethod
    def add_tests(
        self,
        new_tests_description: str,
        context: list[Context],
        existing_test_code: Optional[str] = None
    ) -> str:
        ...

class ImplementationCodeGenerator(ABC):
    @abstractmethod
    def implement(
        self,
        test_code: str,
        context: list[Context],
        existing_production_code: Optional[str] = None
    ) -> str:
        ...

class RefactoredTestCodeGenerator(ABC):
    @abstractmethod
    def refactor_test_code(
        self,
        test_code: str,
        refactor_goal: str,
        context: list[Context]
    ) -> str:
        ...

class RefactoredProductionCodeGenerator(ABC):
    @abstractmethod
    def refactor_production_code(
        self,
        test_code: str,
        production_code: str,
        refactor_goal: str,
        context: list[Context]
    ) -> str:
        ...

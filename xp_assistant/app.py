from logging import Logger

from xp_assistant.add_behavior_step import AddBehaviorStep
from xp_assistant.refactor_step import RefactorStep
from xp_assistant.source_code import SourceCodePair
from xp_assistant.version_control.version_control import VersionControl


class App:
    def __init__(
        self,
        version_control: VersionControl,
        logger: Logger
    ):
        self._version_control = version_control
        self._logger = logger

    def run(self, source_code_pair: SourceCodePair):
        while True:
            print(f'Working on {source_code_pair.production_code.file_path}')
            print('========================================================')
            print('"A": Add behavior')
            print('"R": Refactor')
            print('"T": Refactor tests')
            choice = input("Enter choice: ").strip().lower()

            if choice == "a":
                AddBehaviorStep(self._version_control, self._logger).run(source_code_pair)
                continue
            elif choice == 'r':
                RefactorStep(
                    self._version_control,
                    self._logger
                ).run(source_code_pair)
            elif choice == 't':
                RefactorStep(
                    self._version_control,
                    self._logger
                ).run(SourceCodePair(test_code=source_code_pair.test_code, production_code=source_code_pair.test_code))
            else:
                print("Invalid choice, please try again.")

from logging import Logger

from tcr_assistant.add_behavior_step import AddBehaviorStep
from tcr_assistant.source_code import SourceCodePair
from tcr_assistant.version_control.version_control import VersionControl


class App:
    def __init__(
        self,
        version_control: VersionControl,
        logger: Logger,
        add_behavior_step: AddBehaviorStep
    ):
        self._version_control = version_control
        self._logger = logger
        self._add_behavior_step = add_behavior_step

    def run(self, source_code_pair: SourceCodePair):
        if source_code_pair.production_code.is_empty():
            self._add_behavior_step.run(source_code_pair)

        while True:
            print('========================================================')
            print(f'Working on {source_code_pair.production_code.file_path}')
            print('========================================================')
            print('"B": Add behavior')
            print('"P": Refactor production code')
            print('"T": Refactor test code')
            choice = input("Enter choice: ").strip().lower()

            if choice == "b":
                self._add_behavior_step.run(source_code_pair)
                continue
            elif choice == 'p':
                raise NotImplementedError
            elif choice == 't':
                raise NotImplementedError
            else:
                print("Invalid choice, please try again.")

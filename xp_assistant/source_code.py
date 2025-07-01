from dataclasses import dataclass


@dataclass(frozen=True)
class SourceCodeFile:
    project_path: str
    file_path: str

    def read_code(self) -> str:
        with open(f'{self.project_path}/{self.file_path}') as f:
            return f.read()

    def write_code(self, code: str) -> None:
        with open(f'{self.project_path}/{self.file_path}', 'wb') as f:
            f.write(code.encode())


@dataclass(frozen=True)
class SourceCodePair:
    production_code: SourceCodeFile
    test_code: SourceCodeFile


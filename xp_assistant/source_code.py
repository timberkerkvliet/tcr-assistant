from dataclasses import dataclass


@dataclass(frozen=True)
class SourceCodeFile:
    project_path: str
    file_path: str

    def name(self) -> str:
        return self.file_path.split('/')[-1].split('.')[0]

    def read_code(self) -> str:
        try:
            with open(f'{self.project_path}/{self.file_path}') as f:
                return f.read()
        except FileNotFoundError:
            return ''

    def is_empty(self) -> bool:
        return len(self.read_code()) == 0

    def write_code(self, code: str) -> None:
        with open(f'{self.project_path}/{self.file_path}', 'wb') as f:
            f.write(code.encode())


@dataclass(frozen=True)
class SourceCodePair:
    production_code: SourceCodeFile
    test_code: SourceCodeFile
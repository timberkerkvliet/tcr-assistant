from abc import ABC
from dataclasses import dataclass

from build.lib.tcr_assistant.source_code import SourceCodeFile


class Context(ABC):
    pass


@dataclass
class ProductionCodeFile:
    file: SourceCodeFile


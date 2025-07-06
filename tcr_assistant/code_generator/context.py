from __future__ import annotations

from typing import Iterator, TypeVar

from tcr_assistant.code_generator.context_element import ContextElement


class Context:
    def __init__(self, elements: list[ContextElement]):
        self._elements = elements

    @staticmethod
    def empty():
        return Context([])

    @staticmethod
    def with_element(element: ContextElement):
        return Context([element])

    def add_element(self, context_element: ContextElement) -> Context:
        return Context(self._elements + [context_element])


    def add_elements(self, context_elements: list[ContextElement]) -> Context:
        return Context(self._elements + context_elements)

    def __iter__(self) -> Iterator[ContextElement]:
        return iter(self._elements)

    def map(self, context_mapper: ContextMapper):
        return context_mapper.map(self)

T = TypeVar('T')

class ContextMapper:
    def __init__(
        self,
        mappers
    ):
        self._mappers = mappers

    def map(self, context: Context) -> list[str]:
        return [self.map_element(element) for element in context]

    def map_element(self, context_element: ContextElement) -> str:
        if type(context_element) not in self._mappers:
            raise KeyError(f'No mapper for {type(context_element)}')

        mapper = self._mappers[type(context_element)]

        return mapper(context_element)

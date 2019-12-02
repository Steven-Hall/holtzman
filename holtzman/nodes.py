from typing import Any
from abc import ABC, abstractmethod

from .errors import MissingVariableError


class Node(ABC):
    def __init__(self, value):
        self._value = value
        super().__init__()

    @abstractmethod
    def render(self, variables: Any) -> str:
        pass


class TextNode(Node):
    def __init__(self, value: str):
        super().__init__(value)

    def __repr__(self):
        return f'text node: "{self._value}"'

    def render(self, _variables: Any) -> str:
        return self._value


class VariableNode(Node):
    def __init__(self, value: str):
        self._name_list = value.split(".")
        super().__init__(value)

    def __repr__(self):
        return f'variable node: "{self._value}" ({self._name_list})'

    def render(self, variables: Any) -> str:
        try:
            var = variables
            for word in self._name_list:
                var = var[word]

            return var
        except KeyError:
            raise MissingVariableError(self._value)

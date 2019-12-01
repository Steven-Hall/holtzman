from typing import Dict
from abc import ABC, abstractmethod

from .errors import MissingVariableError


class Node(ABC):
    def __init__(self, value):
        self._value = value
        super().__init__()

    @abstractmethod
    def render(self, variables: Dict[str, str]) -> str:
        pass


class TextNode(Node):
    def __init__(self, value: str):
        super().__init__(value)

    def __repr__(self):
        return f'text node: "{self._value}"'

    def render(self, _variables: Dict[str, str]) -> str:
        return self._value


class VariableNode(Node):
    def __init__(self, value: str):
        super().__init__(value)

    def __repr__(self):
        return f'variable node: "{self._value}"'

    def render(self, _variables: Dict[str, str]) -> str:
        try:
            return _variables[self._value]
        except KeyError:
            raise MissingVariableError(self._value)

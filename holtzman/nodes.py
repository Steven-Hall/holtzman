from typing import Any, List
from abc import ABC, abstractmethod

from .errors import MissingVariableError


class Node(ABC):
    @abstractmethod
    def render(self, variables: Any) -> str:
        pass


class TextNode(Node):
    def __init__(self, value):
        self._value = value
        super().__init__()

    def __repr__(self):
        return f'text node: "{self._value}"'

    def render(self, _variables: Any) -> str:
        return self._value


class VariableNode(Node):
    def __init__(self, value: str):
        self._name_list: List[str] = value.split(".")
        super().__init__()

    def __repr__(self):
        return f'variable node: ({self._name_list})'

    def render(self, variables: Any) -> str:
        var = variables

        try:
            for word in self._name_list:
                if isinstance(var, dict):
                    var = var[word]
                else:
                    var = getattr(var, word)
            return var
        except KeyError:
            raise MissingVariableError(word)


class ForLoopNode(Node):
    def __init__(self, var_name: str, collection_name: str, child_nodes: List[Node]):
        self._var_name: str = var_name
        self._collection_name: str = collection_name
        self._child_nodes: List[Node] = child_nodes
        super().__init__()

    def __repr__(self):
        return f'for loop node: "{self._var_name}" in "{self._collection_name}"'

    def render(self, variables: Any) -> str:
        return ""

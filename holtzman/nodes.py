from typing_extensions import Protocol
from typing import List, Any

from .errors import MissingVariableError


class Node(Protocol):
    def render(self, variables: Any) -> str:
        pass


class RootNode:
    def __init__(self):
        self._children: List[Node] = []

    def add_child(self, child: Node) -> None:
        self._children.append(child)

    def __repr__(self) -> str:
        return f'root node: {self._children}]'

    def render(self, variables: Any) -> str:
        result = []
        for node in self._children:
            result.append(node.render(variables))
        return ''.join(result)


class TextNode:
    def __init__(self, text: str):
        self._text = text

    def __repr__(self) -> str:
        return f'text node: {self._text[0:20]}'

    def render(self, _variables: Any) -> str:
        return self._text


class VariableNode:
    def __init__(self, variable_name_list: List[str]):
        self._variable_name_list: List[str] = variable_name_list

    def __repr__(self) -> str:
        return f'variable node: {self._variable_name_list}'

    def render(self, variables: Any) -> str:
        var = variables
        for variable_name in self._variable_name_list:
            try:
                if isinstance(var, dict):
                    var = var[variable_name]
                else:
                    var = getattr(var, variable_name)
            except (KeyError, AttributeError):
                raise MissingVariableError(variable_name)
        return var

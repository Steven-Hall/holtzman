from typing_extensions import Protocol
from typing import List

from .variables import VariableContext


class Node(Protocol):
    def render(self, variables: VariableContext) -> str:
        pass


class RootNode:
    def __init__(self):
        self._children: List[Node] = []

    def add_child(self, child: Node) -> None:
        self._children.append(child)

    def __repr__(self) -> str:
        return f'root node: {self._children}]'

    def render(self, variables: VariableContext) -> str:
        result = []
        for node in self._children:
            result.append(node.render(variables))
        return ''.join(result)


class TextNode:
    def __init__(self, text: str):
        self._text = text

    def __repr__(self) -> str:
        return f'text node: "{self._text[0:20]}"'

    def render(self, _variables: VariableContext) -> str:
        return self._text


class VariableNode:
    def __init__(self, variable_name: str):
        self._variable_name: str = variable_name

    def __repr__(self) -> str:
        return f'variable node: {self._variable_name}'

    def render(self, variables: VariableContext) -> str:
        return variables[self._variable_name].__str__()


class IfConditionNode(RootNode):
    def __init__(self, variable_name: str):
        self._variable_name: str = variable_name
        self._children: List[Node] = []

    def __repr__(self) -> str:
        return f'if condition node: {self._variable_name}'

    def render(self, variables: VariableContext) -> str:
        var = variables[self._variable_name]

        if var:
            result = []
            for child_node in self._children:
                result.append(child_node.render(variables))
            return ''.join(result)
        return ''


class ForLoopNode(RootNode):
    def __init__(self, variable_name: str, collection_name: str):
        self._variable_name = variable_name
        self._collection_name = collection_name
        self._children: List[Node] = []

    def __repr__(self) -> str:
        return f'for loop node: {self._variable_name}: {self._collection_name}'

    def render(self, variables: VariableContext) -> str:
        collection = variables[self._collection_name]

        result: List[str] = []
        for variable in collection:
            variables.push_context({self._variable_name: variable})
            for child in self._children:
                result.append(child.render(variables))
            variables.pop_context()
        return ''.join(result)

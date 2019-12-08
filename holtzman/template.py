from typing import Any

from .nodes import RootNode
from .variables import VariableContext


class Template:
    def __init__(self, root_node: RootNode):
        self._root_node: RootNode = root_node

    def render(self, variables: Any) -> str:
        return self._root_node.render(VariableContext(variables))

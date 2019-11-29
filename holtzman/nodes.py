from typing import Dict


class TextNode:
    def __init__(self, value: str):
        self._value = value

    def __repr__(self):
        return f'text node: "{self._value}"'

    def render(self, _variables: Dict[str, str]) -> str:
        return self._value

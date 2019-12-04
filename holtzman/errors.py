from typing import Tuple


class TemplateError(Exception):
    def __init__(self, message: str, position: Tuple[int, int]):
        self._message: str = message
        self._line: int = position[0]
        self._column: int = position[1]
        super().__init__()

    @property
    def message(self) -> str:
        return self._message

    @property
    def line(self) -> int:
        return self._line

    @property
    def column(self) -> int:
        return self._column

    def __repr__(self) -> str:
        return f"{self._line}:{self._column}:{self._message}"


class MissingVariableError(Exception):
    def __init__(self, variable: str):
        self._variable: str = variable
        super().__init__()

    @property
    def variable(self) -> str:
        return self._variable

from typing import Tuple

from enum import Enum, auto


class ErrorCode(Enum):
    INVALID_TEMPLATE_STRING = auto()
    MISSING_END_STATEMENT = auto()
    UNEXPECTED_END_STATEMENT = auto()
    INVALID_ESCAPE_SEQUENCE = auto()
    EMPTY_VARIABLE_STRING = auto()
    INVALID_VARIABLE_NAME = auto()
    INVALID_FOR_LOOP = auto()


class TemplateError(Exception):
    def __init__(self, error_code: ErrorCode, position: Tuple[int, int]):
        self._error_code: ErrorCode = error_code
        self._position: Tuple[int, int] = position
        super().__init__()

    @property
    def error_code(self) -> ErrorCode:
        return self._error_code

    @property
    def position(self) -> Tuple[int, int]:
        return self._position

    def __repr__(self) -> str:
        return f"{self._position}:{self._error_code}"


class MissingVariableError(Exception):
    def __init__(self, variable: str):
        self._variable: str = variable
        super().__init__()

    @property
    def variable(self) -> str:
        return self._variable

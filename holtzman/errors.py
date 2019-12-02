class TemplateError(Exception):
    def __init__(self, message: str, *, line: int, column: int):
        self._message: str = message
        self._line: int = line
        self._column: int = column
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


class MissingVariableError(Exception):
    def __init__(self, variable: str):
        self._variable: str = variable
        super().__init__()

    @property
    def variable(self) -> str:
        return self._variable

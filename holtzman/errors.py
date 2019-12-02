class TemplateError(Exception):
    def __init__(self, *, line: int, column: int):
        super().__init__()
        self._line: int = line
        self._column: int = column

    @property
    def line(self) -> int:
        return self._line

    @property
    def column(self) -> int:
        return self._column


class InvalidVariableStringError(TemplateError):
    pass


class InvalidLoopStringError(TemplateError):
    pass


class MissingVariableError(Exception):
    def __init__(self, variable):
        super().__init__()
        self._variable = variable

    @property
    def variable(self) -> str:
        return self._variable

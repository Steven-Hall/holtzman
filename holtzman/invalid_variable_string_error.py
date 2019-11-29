class InvalidVariableStringError(Exception):
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

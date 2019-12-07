from typing import Tuple
from .input_stream import InputStream


class TemplateSource:
    def __init__(self, source: InputStream):
        self._source = source
        self._line = 1
        self._column = 1
        self._next_char = ''
        self._current_char = ''
        self.read_char()

    @property
    def current_char(self) -> str:
        return self._current_char

    @property
    def next_char(self) -> str:
        return self._next_char

    @property
    def position(self) -> Tuple[int, int]:
        return (self._line, self._column)

    def read_char(self) -> None:
        self._current_char = self._next_char
        self._next_char = self._source.read(1)
        if self._current_char == "\n":
            self._line += 1
            self._column = 1
        else:
            self._column += 1

from typing import Tuple, List
from .input_stream import InputStream


class TemplateSource:
    def __init__(self, source: InputStream):
        self._source: InputStream = source
        self._line: int = 1
        self._column: int = 1
        self._next_char: str = ''
        self._current_char: str = ''
        self._bookmarks: List[Tuple[int, int]] = [(1, 1)]
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

    @property
    def bookmark(self) -> Tuple[int, int]:
        return self._bookmarks[-1]

    def read_char(self) -> None:
        self._current_char = self._next_char
        self._next_char = self._source.read(1)
        if self._current_char == "\n":
            self._line += 1
            self._column = 1
        else:
            self._column += 1

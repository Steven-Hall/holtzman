from io import StringIO

from typing import Dict, List
from typing_extensions import Protocol

from .invalid_variable_string_error import InvalidVariableStringError
from .nodes import TextNode


class InputStream(Protocol):
    def read(self, number: int) -> str:
        pass


class Template:
    @staticmethod
    def from_string(source: str) -> 'Template':
        source_stream: StringIO = StringIO(source)
        return Template(source_stream)

    def __init__(self, source: InputStream):
        self._source: InputStream = source
        self._text_buffer: List[str] = []
        self._nodes: List[TextNode] = []

        self._line = 1
        self._column = 1

        self._read_char()
        self._parse_template()

    def render(self, variables: Dict[str, str]) -> str:
        buffer: List[str] = []
        for node in self._nodes:
            buffer.append(node.render(variables))

        return ''.join(buffer)

    def _read_char(self) -> None:
        self._current_char = self._source.read(1)
        if self._current_char == '\n':
            self._line += 1
            self._column = 1
        else:
            self._column += 1

    def _read_variable_name(self) -> None:
        # skip over whitespace
        while self._current_char.isspace():
            self._read_char()

        while self._current_char.isalpha():
            self._read_char()

        # skip over whitespace
        while self._current_char.isspace():
            self._read_char()

        if self._current_char != '}':
            raise InvalidVariableStringError(line=self._line, column=self._column)

        self._read_char()

        if self._current_char != '}':
            raise InvalidVariableStringError(line=self._line, column=self._column)

    def _read_variable_string(self) -> None:
        self._read_char()

        if self._current_char != '{':
            # not really a variable string so stop
            return

        self._nodes.append(TextNode(''.join(self._text_buffer)))
        self._text_buffer = []

        self._read_char()

        while self._current_char.isspace():
            self._read_char()
            self._read_variable_name()

    def _read_escaped_char(self) -> None:
        self._read_char()

        # for the patterns \\ and \{
        # pop the \ from the buffer so they become \ and {
        # ignore everything else
        if self._current_char in ['\\', '{']:
            self._text_buffer.pop()

    def _parse_template(self) -> None:
        while self._current_char != '':
            self._text_buffer.append(self._current_char)
            if self._current_char == '{':
                self._read_variable_string()
            elif self._current_char == '\\':
                self._read_escaped_char()
            else:
                self._read_char()

        self._nodes.append(TextNode(''.join(self._text_buffer)))

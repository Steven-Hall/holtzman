from io import StringIO

from typing import Dict, List
from typing_extensions import Protocol

from .errors import TemplateError
from .nodes import Node, TextNode, VariableNode


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
        self._nodes: List[Node] = []

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

    def _read_variable_name(self) -> str:
        start_line: int = self._line
        start_column: int = self._column

        variable_name: List[str] = []

        if not self._current_char.isalpha():
            raise TemplateError("invalid variable name", line=start_line, column=start_column)

        while self._current_char.isalnum() or self._current_char in ['_', '.']:
            variable_name.append(self._current_char)
            self._read_char()

        return ''.join(variable_name)

    def _eat_whitespace(self):
        while self._current_char.isspace() and self._current_char != '':
            self._read_char()

    def _read_variable_string(self) -> None:
        start_line: int = self._line
        start_column: int = self._column - 2

        # pop off the last '{'
        self._text_buffer.pop()

        self._nodes.append(TextNode(''.join(self._text_buffer)))
        self._text_buffer = []

        self._read_char()

        while self._current_char.isspace():
            self._read_char()
        variable_name: str = self._read_variable_name()

        self._nodes.append(VariableNode(''.join(variable_name)))

        self._eat_whitespace()

        first = self._current_char
        self._read_char()
        second = self._current_char

        if (first != '}') or (second != '}'):
            raise TemplateError("invalid variable string", line=start_line, column=start_column)

        self._read_char()

    def _read_escaped_char(self) -> None:
        self._read_char()

        # for the patterns \\ and \{
        # pop the \ from the buffer so they become \ and {
        # ignore everything else
        if self._current_char in ['\\', '{']:
            self._text_buffer.pop()

    def _read_keyword(self) -> str:
        buffer: List[str] = []
        while not self._current_char.isspace() and self._current_char != '':
            buffer.append(self._current_char)
            self._read_char()

        return ''.join(buffer)

    def _read_loop_string(self) -> None:
        start_line: int = self._line
        start_column: int = self._column - 2

        # pop off the '%'
        self._text_buffer.pop()

        self._nodes.append(TextNode(''.join(self._text_buffer)))
        self._text_buffer = []

        self._read_char()

        self._eat_whitespace()

        keyword = self._read_keyword()

        # TODO keyword == 'end' is also valid here when a loop ends
        if keyword != 'for':
            raise TemplateError("invalid loop string", line=start_line, column=start_column)

        self._eat_whitespace()

        self._read_variable_name()

        self._eat_whitespace()

        keyword = self._read_keyword()

        if keyword != 'in':
            raise TemplateError("invalid loop string", line=start_line, column=start_column)

        self._eat_whitespace()

        self._read_variable_name()

        self._read_char()
        first = self._current_char
        self._read_char()
        second = self._current_char

        if first != '%' or second != '}':
            raise TemplateError("invalid loop string", line=start_line, column=start_column)

    def _read_template_string(self) -> None:
        self._read_char()

        if self._current_char == '{':
            self._read_variable_string()
        elif self._current_char == '%':
            self._read_loop_string()

        # otherwise the string is not really a template string, so do nothing

    def _parse_template(self) -> None:
        while self._current_char != '':
            self._text_buffer.append(self._current_char)
            if self._current_char == '{':
                self._read_template_string()
            elif self._current_char == '\\':
                self._read_escaped_char()
            else:
                self._read_char()

        self._nodes.append(TextNode(''.join(self._text_buffer)))

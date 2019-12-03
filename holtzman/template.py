from io import StringIO

from typing import Dict, List
from typing_extensions import Protocol

from .errors import TemplateError
from .nodes import RootNode, TextNode, VariableNode


class InputStream(Protocol):
    def read(self, number: int) -> str:
        pass


class Template:
    @staticmethod
    def from_string(source: str) -> "Template":
        source_stream: StringIO = StringIO(source)
        return Template(source_stream)

    def __init__(self, source: InputStream):
        self._source: InputStream = source
        self._current_char: str = ''
        self._buffer: List[str] = []
        self._line: int = 1
        self._column: int = 1

        self._current_node: RootNode = RootNode()
        self._node_stack: List[RootNode] = []
        self._parse_template()

    def _handle_escape_char(self) -> None:
        line = self._line
        column = self._column
        self._read_char()
        if self._current_char == '{':
            self._buffer.append('{')
        elif self._current_char == '\\':
            self._buffer.append('\\')
        else:
            raise TemplateError('invalid escape sequence: "\\{self._current_char}"', line=line, column=column)

    def _parse_template(self) -> None:
        self._read_char()

        while self._current_char != '':
            if self._current_char == "{":
                self._handle_template_string()
            elif self._current_char == "\\":
                self._handle_escape_char()
            else:
                self._buffer.append(self._current_char)
            self._read_char()
        self._create_text_node(''.join(self._buffer))

    def _create_text_node(self, value: str) -> None:
        self._current_node.add_child(TextNode(value))

    def _consume_space(self) -> None:
        # skip characters until we find a non-space char or EOF
        while self._current_char.isspace() and self._current_char != '':
            self._read_char()

    def _read_until_space(self) -> str:
        buffer: List[str] = []
        while (not self._current_char.isspace()) and self._current_char != '':
            buffer.append(self._current_char)
            self._read_char()
        return ''.join(buffer)

    def _read_variable_name(self) -> List[str]:
        buffer: List[str] = []
        while self._current_char in ["_", "."] or self._current_char.isalnum():
            buffer.append(self._current_char)
            self._read_char()
        return ''.join(buffer).split(".")

    def _handle_for_loop(self) -> None:
        pass

    def _handle_if_condition(self) -> None:
        pass

    def _handle_variable(self):
        line = self._line
        column = self._column - 2  # count from the first {
        if self._current_char != '{':
            return

        self._read_char()
        self._consume_space()
        variable_name_list = self._read_variable_name()
        self._consume_space()

        first: str = self._current_char
        self._read_char()
        second: str = self._current_char

        if first != '}' or second != '}':
            raise TemplateError('variable string does not end with "}}"', line=line, column=column)

        self._current_node.add_child(VariableNode(variable_name_list))

    def _handle_if_or_loop(self) -> None:
        self._read_char()  # consume the %
        self._consume_space()

        keyword = self._read_until_space()
        if keyword == 'for':
            self._handle_for_loop()
        elif keyword == 'if':
            self._handle_if_condition()
        else:
            raise TemplateError(f'Unexpected Keyword {keyword}', line=self._line, column=self._column)

    def _handle_template_string(self) -> None:
        self._read_char()
        if self._current_char == '%':
            self._create_text_node(''.join(self._buffer))
            self._buffer = []
            self._handle_if_or_loop()
        elif self._current_char == '{':
            self._create_text_node(''.join(self._buffer))
            self._buffer = []
            self._handle_variable()
        else:
            # otherwise not a real template string so add the
            # already read characters onto the buffer and return
            self._buffer.append('{')
            self._buffer.append(self._current_char)

    def _read_char(self) -> None:
        self._current_char = self._source.read(1)
        if self._current_char == "\n":
            self._line += 1
            self._column = 1
        else:
            self._column += 1

    def render(self, variables: Dict[str, str]) -> str:
        return self._current_node.render(variables)

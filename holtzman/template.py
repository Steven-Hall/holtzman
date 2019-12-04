from io import StringIO

from typing import Dict, List, Tuple
from typing_extensions import Protocol

from .errors import TemplateError
from .nodes import RootNode, TextNode, VariableNode, IfConditionNode


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
        self._token_string_column = 1
        self._token_string_line = 1

        self._current_node: RootNode = RootNode()
        self._node_stack: List[Tuple[RootNode, int, int]] = []

        self._parse_template()

        if len(self._node_stack) != 0:
            raise TemplateError("missing end statement in template", line=self._token_string_line, column=self._token_string_column)

    def _push_node(self) -> None:
        self._node_stack.append((self._current_node, self._token_string_line, self._token_string_column))

    def _pop_node(self) -> RootNode:
        if len(self._node_stack) == 0:
            raise TemplateError("unexpected end statement", line=self._token_string_line, column=self._token_string_column)
        (node, line, column) = self._node_stack.pop()
        node.add_child(self._current_node)
        self._token_string_line = line
        self._token_string_column = column
        return node

    def _handle_escape_char(self) -> None:
        self._token_string_line = self._line
        self._token_string_column = self._column

        self._read_char()
        if self._current_char == '{':
            self._buffer.append('{')
        elif self._current_char == '\\':
            self._buffer.append('\\')
        else:
            raise TemplateError('invalid escape sequence: "\\{self._current_char}"', line=self._token_string_line, column=self._token_string_column)

    def _parse_template(self) -> None:
        self._read_char()

        while self._current_char != '':
            if self._current_char == "{":
                # TODO store the clause line and clause column in the stack (useful for error messages)
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
        self._token_string_line = self._line
        self._token_string_column = self._column
        buffer: List[str] = []
        while self._current_char in ["_", "."] or self._current_char.isalnum():
            buffer.append(self._current_char)
            self._read_char()

        if len(buffer) == 0:
            raise TemplateError("empty template string", line=self._token_string_line, column=self._token_string_column)
        return ''.join(buffer).split(".")

    def _handle_for_loop(self) -> None:
        pass

    def _handle_if_condition(self) -> None:
        self._token_string_line = self._line
        self._token_string_column = self._column

        self._consume_space()
        variable_name_list = self._read_variable_name()
        self._consume_space()

        first = self._current_char
        self._read_char()
        second = self._current_char

        if first != '%' or second != '}':
            raise TemplateError("if template string is not closed", line=self._token_string_line, column=self._token_string_column)

        self._push_node()
        self._current_node = IfConditionNode(variable_name_list)

    def _handle_variable(self):
        self._token_string_line = self._line
        self._token_string_column = self._column - 2  # count from the first {
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
            raise TemplateError('variable string does not end with "}}"', line=self._token_string_line, column=self._token_string_column)

        self._current_node.add_child(VariableNode(variable_name_list))

    def _handle_end_statement(self):
        self._token_string_line = self._line
        self._token_string_column = self._column

        self._consume_space()
        first = self._current_char
        self._read_char()
        second = self._current_char

        if first != '%' or second != '}':
            raise TemplateError('variable end string does not end with "%}"', line=self._token_string_line, column=self._token_string_column)

        self._current_node = self._pop_node()

    def _handle_if_or_loop(self) -> None:
        self._read_char()  # consume the %
        self._consume_space()

        keyword = self._read_until_space()
        if keyword == 'for':
            self._handle_for_loop()
        elif keyword == 'if':
            self._handle_if_condition()
        elif keyword == 'end':
            self._handle_end_statement()
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

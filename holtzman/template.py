from io import StringIO

from typing import List, Tuple, Any
from typing_extensions import Protocol

from .errors import TemplateError
from .nodes import RootNode, TextNode, VariableNode, IfConditionNode, ForLoopNode
from .variables import VariableContext


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

        # use to keep useful error information
        # generally when an error occurs we want the start of the token string
        # not the current position
        self._error_positions: List[Tuple[int, int]] = []
        self._error_position: Tuple[int, int] = (1, 1)

        self._current_node: RootNode = RootNode()
        self._node_stack: List[Tuple[RootNode, Tuple[int, int]]] = []

        self._parse_template()

        if len(self._node_stack) != 0:
            raise TemplateError("missing end statement in template", (self._error_position))

    def _push_node(self) -> None:
        self._node_stack.append((self._current_node, self._error_position))

    def _pop_node(self) -> RootNode:
        if len(self._node_stack) == 0:
            raise TemplateError("unexpected end statement", self._error_position)
        (node, error_position) = self._node_stack.pop()
        node.add_child(self._current_node)
        self._error_position = error_position
        return node

    def _handle_escape_char(self) -> None:
        self._error_position = (self._line, self._column)

        self._read_char()
        if self._current_char == '{':
            self._buffer.append('{')
        elif self._current_char == '\\':
            self._buffer.append('\\')
        else:
            raise TemplateError('invalid escape sequence: "\\{self._current_char}"', self._error_position)

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
        if len(value) > 0:
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

    def _read_variable_name(self) -> str:
        self._error_position = (self._line, self._column)
        buffer: List[str] = []
        while self._current_char in ["_", "."] or self._current_char.isalnum():
            buffer.append(self._current_char)
            self._read_char()

        if len(buffer) == 0:
            raise TemplateError("empty template string", self._error_position)
        return ''.join(buffer)

    def _read_end_statement(self, expected: str) -> None:
        first: str = self._current_char
        self._read_char()
        second: str = self._current_char

        if ''.join([first, second]) != expected:
            raise TemplateError("template string is not closed", self._error_position)

    def _handle_for_loop(self) -> None:
        self._error_position = (self._line, self._column)

        self._consume_space()
        variable_name = self._read_variable_name()

        if len(variable_name.split('.')) != 1:
            raise TemplateError("invalid variable name in for loop", self._error_position)

        variable_name = variable_name[0]

        self._consume_space()

        keyword: str = self._read_until_space()

        if keyword != 'in':
            raise TemplateError('for statement missing "in"', self._error_position)

        self._consume_space()

        collection_name = self._read_variable_name()

        self._consume_space()

        self._read_end_statement("%}")

        self._push_node()
        self._current_node = ForLoopNode(variable_name, collection_name)

    def _handle_if_condition(self) -> None:
        self._error_position = (self._line, self._column)

        self._consume_space()
        variable_name_list = self._read_variable_name()
        self._consume_space()

        self._read_end_statement("%}")

        self._push_node()
        self._current_node = IfConditionNode(variable_name_list)

    def _handle_variable(self):
        # count the column from the opening {
        self._error_position = (self._line, self._column - 2)

        self._read_char()
        self._consume_space()
        self._error_positions.append(self._error_position)

        variable_name_list = self._read_variable_name()

        self._error_position = self._error_positions.pop()
        self._consume_space()

        self._read_end_statement("}}")

        self._current_node.add_child(VariableNode(variable_name_list))

    def _handle_end_statement(self):
        self._error_position = (self._line, self._column)

        self._consume_space()

        self._read_end_statement("%}")

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
            raise TemplateError(f'Unexpected Keyword {keyword}', self._error_position)

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

    def render(self, variables: Any) -> str:
        return self._current_node.render(VariableContext(variables))

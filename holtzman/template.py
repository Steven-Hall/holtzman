from io import StringIO

from typing import List, Any, TextIO

from .errors import TemplateError
from .nodes import RootNode, TextNode, VariableNode, IfConditionNode, ForLoopNode
from .variables import VariableContext
from .template_source import TemplateSource


class Template:
    @staticmethod
    def from_string(source: str) -> "Template":
        source_stream: StringIO = StringIO(source)
        template_source = TemplateSource(source_stream)
        return Template(template_source)

    @staticmethod
    def from_file(source_file: str) -> "Template":
        source_stream: TextIO = open(source_file, 'r')
        try:
            template_source = TemplateSource(source_stream)
            return Template(template_source)
        finally:
            source_stream.close()

    def __init__(self, source: TemplateSource):
        self._source: TemplateSource = source
        self._buffer: List[str] = []
        self._current_node: RootNode = RootNode()
        self._node_stack: List[RootNode] = []
        self._parse_template()

        if len(self._node_stack) != 0:
            raise TemplateError("missing end statement in template", self._source.position)

    def _push_node(self) -> None:
        self._node_stack.append(self._current_node)

    def _pop_node(self) -> RootNode:
        if len(self._node_stack) == 0:
            raise TemplateError("unexpected end statement", self._source.position)
        node = self._node_stack.pop()
        node.add_child(self._current_node)
        return node

    def _handle_escape_char(self) -> None:
        # pylint: disable=raising-format-tuple
        self._source.read_char()
        if self._source.current_char == '{':
            self._buffer.append('{')
        elif self._source.current_char == '\\':
            self._buffer.append('\\')
        else:
            raise TemplateError('invalid escape sequence: "\\{self._current_char}"',
                                self._source.position)

    def _parse_template(self) -> None:
        self._source.read_char()
        while self._source.current_char != '':
            if self._source.current_char == "{":
                self._handle_template_string()
            elif self._source.current_char == "\\":
                self._handle_escape_char()
            else:
                self._buffer.append(self._source.current_char)
            self._source.read_char()
        self._create_text_node(''.join(self._buffer))

    def _create_text_node(self, value: str) -> None:
        if len(value) > 0:
            self._current_node.add_child(TextNode(value))

    def _consume_space(self) -> None:
        # skip characters until we find a non-space char or EOF
        while self._source.current_char.isspace() and self._source.current_char != '':
            self._source.read_char()

    def _read_until_space(self) -> str:
        buffer: List[str] = []
        while (not self._source.current_char.isspace() and self._source.current_char != ''):
            buffer.append(self._source.current_char)
            self._source.read_char()
        return ''.join(buffer)

    def _read_variable_name(self) -> str:
        buffer: List[str] = []
        while self._source.current_char in ["_", "."] or self._source.current_char.isalnum():
            buffer.append(self._source.current_char)
            self._source.read_char()

        if len(buffer) == 0:
            raise TemplateError("empty template string", self._source.position)
        return ''.join(buffer)

    def _read_end_statement(self, expected: str) -> None:
        first: str = self._source.current_char
        self._source.read_char()
        second: str = self._source.current_char

        if ''.join([first, second]) != expected:
            raise TemplateError("template string is not closed", self._source.position)

    def _handle_for_loop(self) -> None:
        self._consume_space()
        variable_name = self._read_variable_name()

        if len(variable_name.split('.')) != 1:
            raise TemplateError("invalid variable name in for loop", self._source.position)

        self._consume_space()

        keyword: str = self._read_until_space()

        if keyword != 'in':
            raise TemplateError('for statement missing "in"', self._source.position)

        self._consume_space()
        collection_name = self._read_variable_name()
        self._consume_space()
        self._read_end_statement("%}")
        self._push_node()
        self._current_node = ForLoopNode(variable_name, collection_name)

    def _handle_if_condition(self) -> None:
        self._consume_space()
        variable_name_list = self._read_variable_name()
        self._consume_space()
        self._read_end_statement("%}")
        self._push_node()
        self._current_node = IfConditionNode(variable_name_list)

    def _handle_variable(self):
        self._source.read_char()
        self._consume_space()
        variable_name_list = self._read_variable_name()
        self._consume_space()
        self._read_end_statement("}}")
        self._current_node.add_child(VariableNode(variable_name_list))

    def _handle_end_statement(self):
        self._consume_space()
        self._read_end_statement("%}")
        self._current_node = self._pop_node()

    def _handle_if_or_loop(self) -> None:
        self._source.read_char()  # consume the %
        self._consume_space()

        keyword = self._read_until_space()
        if keyword == 'for':
            self._handle_for_loop()
        elif keyword == 'if':
            self._handle_if_condition()
        elif keyword == 'end':
            self._handle_end_statement()
        else:
            raise TemplateError(f'Unexpected Keyword {keyword}', self._source.position)

    def _handle_template_string(self) -> None:
        self._source.read_char()
        if self._source.current_char == '%':
            self._create_text_node(''.join(self._buffer))
            self._buffer = []
            self._handle_if_or_loop()
        elif self._source.current_char == '{':
            self._create_text_node(''.join(self._buffer))
            self._buffer = []
            self._handle_variable()
        else:
            # otherwise not a real template string so add the
            # already read characters onto the buffer and return
            self._buffer.append('{')
            self._buffer.append(self._source.current_char)

    def render(self, variables: Any) -> str:
        return self._current_node.render(VariableContext(variables))

import pytest

from holtzman.template import Template
from holtzman.errors import TemplateError, ErrorCode


class CompilationErrorHandlingTests:
    def test_missing_end_statement(self):
        with pytest.raises(TemplateError) as error:
            Template.from_string("{% if var %}")

        assert error.value.error_code == ErrorCode.MISSING_END_STATEMENT
        assert error.value.position == (1, 15)

    def test_unexpected_end_statement(self):
        with pytest.raises(TemplateError) as error:
            Template.from_string("1234{% end %}")

        assert error.value.error_code == ErrorCode.UNEXPECTED_END_STATEMENT
        assert error.value.position == (1, 5)

    def test_invalid_escape_sequence(self):
        with pytest.raises(TemplateError) as error:
            Template.from_string("this is \\a invalid")

        assert error.value.error_code == ErrorCode.INVALID_ESCAPE_SEQUENCE
        assert error.value.position == (1, 9)

    def test_empty_variable_string(self):
        with pytest.raises(TemplateError) as error:
            Template.from_string("12345{{ }}")

        assert error.value.error_code == ErrorCode.EMPTY_VARIABLE_STRING
        assert error.value.position == (1, 6)

    def test_missing_closing_brace(self):
        with pytest.raises(TemplateError) as error:
            Template.from_string("12345{{ variable }")

        assert error.value.error_code == ErrorCode.INVALID_TEMPLATE_STRING
        assert error.value.position == (1, 6)

    def test_invalid_variable_name_in_for_loop(self):
        with pytest.raises(TemplateError) as error:
            Template.from_string("{% for invalid.variable in variables %}{% end %}")

        assert error.value.error_code == ErrorCode.INVALID_VARIABLE_NAME
        assert error.value.position == (1, 8)

    def test_invalid_for_loop(self):
        with pytest.raises(TemplateError) as error:
            Template.from_string("12345{% for invalid variables %}{% end %}")

        assert error.value.error_code == ErrorCode.INVALID_FOR_LOOP
        assert error.value.position == (1, 6)

    def test_template_string(self):
        with pytest.raises(TemplateError) as error:
            Template.from_string("12345{% invalid statement %}{% end %}")

        assert error.value.error_code == ErrorCode.INVALID_TEMPLATE_STRING
        assert error.value.position == (1, 6)

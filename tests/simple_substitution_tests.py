"""
Test simple variable substituion, for example:

    {{ variable }}

in a template should be replaced by the variables value in the rendered template
"""
import pytest

from holtzman.template import Template, InvalidVariableStringError


class SimpleSubstitutionTests:
    @pytest.mark.parametrize('source', ['{{ variable', '{{ variable }'])
    def test_invalid_variable_string_throws_error(self, source):
        with pytest.raises(InvalidVariableStringError):
            Template.from_string(source)

    def test_invalid_variable_string_error_includes_line_and_column(self):
        source = "\n\n12345{{ variable }54321\n\n"
        with pytest.raises(InvalidVariableStringError) as error:
            Template.from_string(source)

        assert error.value.line == 3
        assert error.value.column == 20

    def test_single_opening_brace_is_ignored(self):
        source = "{ variable }"
        template = Template.from_string(source)
        result = template.render({'variable': 'test'})
        assert result == "{ variable }"

    def test_escaped_opening_brace_is_replaced(self):
        source = r"\{ variable }"
        template = Template.from_string(source)
        result = template.render({'variable': 'test'})
        assert result == "{ variable }"

    @pytest.mark.skip
    def test_escaped_slash_is_replaced(self): ...

    @pytest.mark.skip
    def test_back_slashes_ignored(self): ...

    @pytest.mark.skip
    def test_variable_is_substituted_correctly(self): ...

    @pytest.mark.skip
    def test_same_variable_is_substituted_multiple_times(self): ...

    @pytest.mark.skip
    def test_multiple_variables_are_substituted_correctly(self): ...

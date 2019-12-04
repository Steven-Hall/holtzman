"""
Test simple variable substituion, for example:

    {{ variable }}

in a template should be replaced by the variables value in the rendered template
"""
import pytest
from collections import namedtuple

from holtzman.template import Template
from holtzman.errors import TemplateError, MissingVariableError


class SimpleSubstitutionTests:
    @pytest.mark.parametrize('source', ['{{ variable', '{{ variable }', '{{ }}'])
    def test_invalid_variable_string_throws_error(self, source):
        with pytest.raises(TemplateError):
            Template.from_string(source)

    @pytest.mark.parametrize('source', ['{{ variable_1 }}'])
    def test_valid_variable_names_do_not_throw_errors(self, source):
        Template.from_string(source)

    def test_invalid_variable_string_error_includes_line_and_column(self):
        source = "\n\n12345{{ variable }54321\n\n"
        with pytest.raises(TemplateError) as error:
            Template.from_string(source)

        assert error.value.line == 3
        assert error.value.column == 6

    def test_single_opening_brace_is_ignored(self):
        source = "{ variable }"
        template = Template.from_string(source)
        result = template.render({})
        assert result == "{ variable }"

    def test_escaped_opening_brace_is_replaced(self):
        source = "\\{ variable }"
        template = Template.from_string(source)
        result = template.render({})
        assert result == "{ variable }"

    def test_escaped_slash_is_replaced(self):
        source = "\\\\ variable \\\\"
        template = Template.from_string(source)
        result = template.render({})
        assert result == "\\ variable \\"

    def test_non_escaped_back_slashes_throw_exceptions(self):
        source = "\\ variable \\"
        with pytest.raises(TemplateError):
            Template.from_string(source)

    def test_variable_is_substituted_correctly(self):
        source = "12345{{   variable   }}12345"
        template = Template.from_string(source)
        result = template.render({"variable": "value"})
        assert result == "12345value12345"

    def test_error_is_thrown_if_template_variable_missing_from_dictionary(self):
        source = "{{ variable }}"
        template = Template.from_string(source)
        with pytest.raises(MissingVariableError) as error:
            template.render({})

        assert error.value.variable == 'variable'

    def test_error_is_thrown_if_template_variable_missing_from_object(self):
        source = "{{ variable }}"
        template = Template.from_string(source)
        Object = namedtuple('Object',  [])
        with pytest.raises(MissingVariableError) as error:
            template.render(Object())

        assert error.value.variable == 'variable'

    def test_same_variable_is_substituted_multiple_times(self):
        source = "{{ variable }} {{ variable }}"
        template = Template.from_string(source)
        result = template.render({"variable": "value"})
        assert result == "value value"

    def test_multiple_variables_are_substituted_correctly(self):
        source = "{{ variable1 }} {{ variable2 }} {{ variable3 }}"
        template = Template.from_string(source)
        result = template.render({
            "variable1": "value_1",
            "variable2": "value_2",
            "variable3": "value_3"
        })
        assert result == "value_1 value_2 value_3"

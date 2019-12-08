"""
if conditions, for example:

    {% if variable %}
        hello world
    {% end %}

in a template should render "hell world" only if variable is True
"""
import pytest

import holtzman
from holtzman.errors import TemplateError


class IfConditionTests:
    @pytest.mark.parametrize('if_string', [
        ("{% if variable"),
        ("{% if variable %"),
        ("{% if %}")])
    def test_invalid_loop_string_throws_error(self, if_string):
        with pytest.raises(TemplateError):
            holtzman.from_string(if_string)

    @pytest.mark.parametrize('if_string', [
        ("{% if var %}{{ var }}"),
        ("{% if var %}{{ var }}{%"),
        ("{% if var %}{{ var }}{% end"),
        ("{% if var %}{{ var }}{% end %")])
    def test_if_condition_missing_valid_end_statement(self, if_string):
        with pytest.raises(TemplateError):
            holtzman.from_string(if_string)

    def test_unexpected_end_causes_error(self):
        source = "{% end %}"
        with pytest.raises(TemplateError):
            holtzman.from_string(source)

    def test_if_condition_renders_if_variable_is_true(self):
        source = "{% if variable %}hello world{% end %}"
        template = holtzman.from_string(source)
        result = template.render({"variable": True})
        assert result == "hello world"

    def test_if_condition_does_not_render_if_variable_is_false(self):
        source = "{% if variable %}hello world{% end %}"
        template = holtzman.from_string(source)
        result = template.render({"variable": False})
        assert result == ""

    def test_if_condition_supports_complex_variable_names(self):
        source = "{% if variable.sub_variable %}hello{% end %}"
        template = holtzman.from_string(source)
        result = template.render({"variable": {"sub_variable": True}})
        assert result == "hello"

    def test_nested_conditions_work(self):
        source = "{% if variable %}{% if variable_2 %}hello{% end %}{% end %}"
        template = holtzman.from_string(source)
        result = template.render({"variable": True, "variable_2": True})
        assert result == "hello"

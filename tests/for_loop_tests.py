"""
for loops, for example:

    {% for variable in variables %}
        {{ variable }}
    {% end %}

in a template should renderer every entry in 'variables'
"""
import pytest

from holtzman.template import Template
from holtzman.errors import TemplateError


class ForLoopTests:
    @pytest.mark.parametrize('loop_string', [
        ("{% for variable in variables"),
        ("{% for variable in variables %"),
        ("{% for variable in %}"),
        ("{% for variable %}"),
        ("{% for"),
        ("{%")])
    def test_invalid_loop_string_throws_error(self, loop_string):
        with pytest.raises(TemplateError):
            Template.from_string(loop_string)

    @pytest.mark.parametrize('loop_string', [
        ("{% for var in vars %}{{ var }}"),
        ("{% for var in vars %}{{ var }}{%"),
        ("{% for var in vars %}{{ var }}{% end"),
        ("{% for var in vars %}{{ var }}{% end %")])
    def test_for_loop_missing_valid_end_statement(self, loop_string):
        with pytest.raises(TemplateError):
            Template.from_string(loop_string)

    def test_unexpected_end_causes_error(self):
        source = "{% end %}"
        with pytest.raises(TemplateError):
            Template.from_string(source)

    def test_for_loop_renders_each_entry_in_collection(self):
        source = "{% for var in variables %}{{ var }}{% end %}"
        template = Template.from_string(source)
        result = template.render({"variables": ["var1", "var2", "var3"]})
        assert result == "var1var2var3"

    def test_for_loop_supports_complex_variable_names(self):
        source = "{% for var in variables.nested %}{{ var }}{% end %}"
        template = Template.from_string(source)
        result = template.render({"variables": {"nested": ["var1", "var2", "var3"]}})
        assert result == "var1var2var3"

    def test_nested_for_loops_work(self):
        source = """
        {% for var in variables %}
            {% for sub_var in var %}
                {{ sub_var }}
            {% end %}
        {% end %}
        """
        variables = [["var1", "var2", "var3"], ["var4", "var5", "var6"]]
        template = Template.from_string(source)
        result = template.render(variables)
        assert result == "var1var2var3var4var5var6"

    def test_child_loop_can_access_parent_variable_in_nested_for_loop(self):
        source = """
        {% for parent_var in parent_variables %}
            {% for child_var in child_variables %}
                {{ parent_var }}
            {% end %}
        {% end %}
        """
        parent_variables = ["parent1", "parent2", "parent3"]
        child_variables = ["child1", "child2", "child3"]
        template = Template.from_string(source)
        result = template.render({"parent_variables": parent_variables, "child_variables": child_variables})
        assert result == "parent1parent2parent3parent1parent2parent3parent1parent2parent3"

    def test_parent_loop_cannot_access_child_variable_in_nested_for_loop(self):
        source = """
        {% for parent_var in parent_variables %}
            {{ child_var }}
            {% for child_var in child_variables %}
            {% end %}
        {% end %}
        """
        with pytest.raises(TemplateError):
            Template.from_string(source)

    def test_child_variable_overrides_parent_variable_with_same_name(self):
        source = """
        {% for var in parent_variables %}
            {% for var in child_variables %}
                {{ var }}
            {% end %}
        {% end %}
        """
        parent_variables = ["parent"]
        child_variables = ["child"]
        template = Template.from_string(source)
        result = template.render({"parent_variables": parent_variables, "child_variables": child_variables})
        assert result == "child"

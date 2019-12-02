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
        ("{% for var in vars %}{{ var }}{% end %"),
        ("{% for var in vars %}{{ var }}{% end %}")])
    def test_for_loop_missing_valid_end_statement(self, loop_string):
        with pytest.raises(TemplateError):
            Template.from_string(loop_string)

    @pytest.mark.skip
    def test_for_loop_renders_each_entry_in_collection(self):
        pass

    @pytest.mark.skip
    def test_for_loop_supports_complex_variable_names(self):
        pass

    @pytest.mark.skip
    def test_nested_for_loops_work(self):
        pass

    @pytest.mark.skip
    def test_child_loop_can_access_parent_variable_in_nested_for_loop(self):
        pass

    @pytest.mark.skip
    def test_parent_loop_cannot_access_child_variable_in_nested_for_loop(self):
        pass

    @pytest.mark.skip
    def test_child_variable_overrides_parent_variable_with_same_name(self):
        pass

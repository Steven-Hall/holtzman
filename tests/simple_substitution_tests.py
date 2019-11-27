"""
Test simple variable substituion, for example:

    {{ variable }}

in a template should be replaced by the variables value in the rendered template
"""
import pytest


@pytest.mark.skip
class SimpleSubstitutionTests:
    def test_invalid_placeholder_throws_error(self): ...

    def test_single_opening_brace_is_ignored(self): ...

    def test_escaped_opening_brace_is_replaced(self): ...

    def test_escaped_slash_is_replaced(self): ...

    def test_back_slashes_ignored(self): ...

    def test_variable_is_substituted_correctly(self): ...

    def test_same_variable_is_substituted_multiple_times(self): ...

    def test_multiple_variables_are_substituted_correctly(self): ...

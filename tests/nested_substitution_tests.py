"""
Test nested variable substituion, for example:

    {{ variable.sub_variable.sub_variable }}

in a template should be replaced by the variables value in the rendered template.
This should work for objects and dictionaries
"""
import pytest


@pytest.mark.skip
class NestedSubstitutionTests:
    def test_object_property_is_substituted_correctly(self): ...

    def test_dictionary_value_is_substituted_correctly(self): ...

"""
Test nested variable substituion, for example:

    {{ variable.sub_variable.sub_variable }}

in a template should be replaced by the variables value in the rendered template.
This should work for objects and dictionaries
"""
from collections import namedtuple

import holtzman


class NestedSubstitutionTests:
    def test_object_property_is_substituted_correctly(self):
        source = "{{ nested.value }}"
        template = holtzman.from_string(source)
        TestObj = namedtuple('TestObj', ['value'])
        obj = TestObj(value="nested_value")
        result = template.render({"nested": obj})

        assert result == "nested_value"

    def test_dictionary_value_is_substituted_correctly(self):
        source = "{{ nested.value }}"
        template = holtzman.from_string(source)
        obj = {"value": "nested_value"}
        result = template.render({"nested": obj})

        assert result == "nested_value"

    def test_dictionary_nested_in_object_is_substituted_correctly(self):
        source = "{{ nested.dictionary.value }}"
        template = holtzman.from_string(source)
        TestObj = namedtuple('TestObj', ['dictionary'])
        dictionary = {'value': 'nested_value'}
        obj = TestObj(dictionary=dictionary)
        result = template.render({"nested": obj})

        assert result == "nested_value"

    def test_object_nested_in_dictionary_is_substituted_correctly(self):
        source = "{{ nested.object.value }}"
        obj = {"value": "nested_value"}
        dictionary = {"object": obj}
        template = holtzman.from_string(source)
        result = template.render({"nested": dictionary})

        assert result == "nested_value"

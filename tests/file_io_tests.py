"""
Test templates can be read from files
"""
import os
import holtzman


class FileIOTests:
    def test_reading_from_template_file(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        test_file = f'{dir_path}/templates/example_template.hz'
        holtzman.from_file(test_file)

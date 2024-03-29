from io import StringIO
from typing import TextIO

from .template import Template
from .template_source import TemplateSource


def from_string(source: str) -> "Template":
    source_stream: StringIO = StringIO(source)
    template_source = TemplateSource(source_stream)
    return Template(template_source)


def from_file(source_file: str) -> "Template":
    source_stream: TextIO = open(source_file, 'r')
    try:
        template_source = TemplateSource(source_stream)
        return Template(template_source)
    finally:
        source_stream.close()

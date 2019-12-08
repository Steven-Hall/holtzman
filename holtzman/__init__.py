from io import StringIO
from typing import TextIO

from .template import Template
from .template_source import TemplateSource
from .template_parser import TemplateParser


def from_string(source: str) -> "Template":
    source_stream: StringIO = StringIO(source)
    template_source = TemplateSource(source_stream)
    template_parser = TemplateParser(template_source)
    return template_parser.parse_template()


def from_file(source_file: str) -> "Template":
    source_stream: TextIO = open(source_file, 'r')
    try:
        template_source = TemplateSource(source_stream)
        template_parser = TemplateParser(template_source)
        return template_parser.parse_template()
    finally:
        source_stream.close()

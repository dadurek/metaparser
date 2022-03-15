import logging

from .modules.auto import ParserFactory

logging.basicConfig(
    format="[%(asctime)s][%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%dT%I:%M:%S",
    level="DEBUG",
)


def entrypoint(filename):
    parser_type = ParserFactory.get_parser_for_file(filename)
    parser = parser_type()
    parser.parse(filename)

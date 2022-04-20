import logging
from typing import Optional, Type

import magic  # type: ignore

from .base import BaseParser
from .exif import ExifParser
from .mp3 import Mp3Parser
from .mp4 import Mp4Parser
from .openXml import OpenXmlParser
from .pdf import PDFParser

PARSERS = [ExifParser, Mp3Parser, PDFParser, Mp4Parser, OpenXmlParser]


class ParserFactory:
    @staticmethod
    def get_parser_for_file(filename: str) -> Optional[Type[BaseParser]]:
        mime = magic.from_file(filename, mime=True)
        logging.debug("Detected MIME type '%s' for file '%s'", mime, filename)

        return ParserFactory.get_parser(mime)

    @staticmethod
    def get_parser(mime) -> Optional[Type[BaseParser]]:
        for parser in PARSERS:
            if mime in parser.supported_mimes():
                return parser

        return None

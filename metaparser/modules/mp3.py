from typing import List

from .base import BaseParser


class Mp3Parser(BaseParser):
    @staticmethod
    def supported_mimes() -> List[str]:
        return ["audio/mpeg"]

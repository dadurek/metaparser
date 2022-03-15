from datetime import datetime
from typing import List, Optional

from PIL import Image  # type: ignore

from .base import BaseParser
from .constants import FIELD_AUTHOR, FIELD_CREATE_DATE


class ExifParser(BaseParser):
    autor: Optional[str]
    create_date: Optional[datetime]
    # TODO: Add more fields

    def __init__(self) -> None:
        super().__init__()
        self.autor = None
        self.create_date = None

    def parse(self, filename: str) -> None:
        img = Image.open(filename)
        exif = img.getexif()
        if 0x0132 in exif:
            self.create_date = datetime.strptime(exif[0x0132], "%Y:%m:%d %H:%M:%S")
        if 0x9C9D in exif:
            self.autor = exif[0x9C9D]

    def get_fields(self) -> List[str]:
        return [FIELD_AUTHOR, FIELD_CREATE_DATE]

    @staticmethod
    def supported_mimes() -> List[str]:
        return ["image/jpeg", "image/png"]

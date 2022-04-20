from typing import Dict, List, Optional

from exif import Image  # type: ignore
from exif._constants import ATTRIBUTE_ID_MAP  # type: ignore

from .base import BaseParser


class ExifParser(BaseParser):
    __img: Image
    __filename: str

    def __init__(self) -> None:
        super().__init__()

    def parse(self, filename: str) -> None:
        self.__filename = filename
        with open(filename, "rb") as f:
            self.__img = Image(f)

    def get_fields(self) -> List[str]:
        return list(ATTRIBUTE_ID_MAP.keys())

    def get_all_values(self) -> Dict[str, str]:
        return self.__img.get_all()

    def set_field(self, field: str, value: Optional[str]) -> None:
        super().set_field(field, value)
        self.__img.set(field, value)

    def delete_field(self, field: str) -> None:
        super().delete_field(field)
        self.__img.delete(field)

    def clear(self) -> None:
        self.__img.delete_all()

    def write(self) -> None:
        with open(self.__filename, "wb") as f:
            f.write(self.__img.get_file())

    @staticmethod
    def supported_mimes() -> List[str]:
        return ["image/jpeg", "image/png"]

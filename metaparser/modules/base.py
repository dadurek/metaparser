from abc import ABC, abstractmethod
from typing import Any, List


class BaseParser(ABC):
    @staticmethod
    @abstractmethod
    def supported_mimes() -> List[str]:
        pass

    @abstractmethod
    def parse(self, filename: str) -> None:
        pass

    @abstractmethod
    def get_fields(self) -> List[str]:
        pass

    def edit_field(self, field: str, value: Any) -> None:
        if field not in self.get_fields():
            raise KeyError("Field not present in parser")
        pass

from abc import ABC, abstractmethod
from typing import Dict, List, Optional


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

    def delete_field(self, field: str) -> None:
        if field not in self.get_fields():
            raise KeyError("Field not present in parser")

    def set_field(self, field: str, value: Optional[str]) -> None:
        if field not in self.get_fields():
            raise KeyError("Field not present in parser")

    @abstractmethod
    def get_all_values(self) -> Dict[str, str]:
        pass

    def clear(self) -> None:
        for field in self.get_fields():
            self.delete_field(field)

    def print(self) -> None:
        items = self.get_all_values().items()
        if len(items) == 0:
            print("No metadata found")
            return

        for v, k in items:
            print(f"{v}: {k}")

    @abstractmethod
    def write(self) -> None:
        pass

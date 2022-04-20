from typing import Any, Dict, List

from PyPDF2 import PdfFileMerger, PdfFileReader  # type: ignore

from .base import BaseParser

FIELD_DISCLAIMER = "You can specify your own fields. Make sure they start with /"
FIELD_TITLE = "/Title"
FIELD_AUTHOR = "/Author"
FIELD_SUBJECT = "/Subject"
FIELD_KEYWORD = "/Keyword"
FIELD_CREATED_DATE = "/Created Date"
FIELD_MODIFIED_DATE = "/Modified Date"
FIELD_CREATOR = "/Creator"
FIELD_PRODUCER = "/Producer"
FIELD_TRAPPED = "/Trapped"


class PDFParser(BaseParser):
    def get_fields(self) -> List[str]:
        return [
            FIELD_DISCLAIMER,
            FIELD_TITLE,
            FIELD_AUTHOR,
            FIELD_SUBJECT,
            FIELD_KEYWORD,
            FIELD_CREATED_DATE,
            FIELD_MODIFIED_DATE,
            FIELD_CREATOR,
            FIELD_PRODUCER,
            FIELD_TRAPPED,
        ]

    @staticmethod
    def supported_mimes() -> List[str]:
        return ["application/pdf", "application/pdf-x"]

    def __init__(self) -> None:
        super().__init__()
        self.metadata: Dict[str, str] = dict()
        self.filename = str()

    def parse(self, filename: str) -> None:
        self.filename = filename
        metadata = PdfFileReader(filename).getDocumentInfo()
        self.metadata = dict()
        for field in metadata:
            self.metadata[field] = metadata[field]

    def set_field(self, field: str, value: Any) -> None:
        super().set_field(field, value)
        if not field.startswith("/"):
            raise ValueError("Bad name for field")
        self.metadata[field] = value

    def delete_field(self, field: str) -> None:
        super().delete_field(field)
        if not field.startswith("/"):
            raise ValueError("Bad name for field")
        del self.metadata[field]

    def write(self) -> None:
        pdf_merger = PdfFileMerger()
        pdf_merger.append(self.filename)
        pdf_merger.addMetadata(self.metadata)
        pdf_merger.write(self.filename)

    def get_all_values(self) -> Dict[str, str]:
        return self.metadata

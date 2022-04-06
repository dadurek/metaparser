from typing import Dict, List, Optional

import zipfile
import xml.etree.ElementTree

from .base import BaseParser

# TODO to doemthing with does FIELDS so provided value will be only 'title' - use dictionary
FIELD_COREPROPERTIES = "{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}coreProperties"
FIELD_TITLE = "{http://purl.org/dc/elements/1.1/}title"
FIELD_SUBJECT = "{http://purl.org/dc/elements/1.1/}subject"
FIELD_CREATOR = "{http://purl.org/dc/elements/1.1/}creator"
FIELD_KEYWORDS = "{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}keywords"
FIELD_DESCRIPTION = "{http://purl.org/dc/elements/1.1/}description"
FIELD_LASTMODIFIEDBY = "{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}lastModifiedBy"
FIELD_REVISION = "{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}revision"
FIELD_CREATED = "{http://purl.org/dc/terms/}created"
FIELD_MODIFIED = "{http://purl.org/dc/terms/}modified"

XML_LOCATION = 'docProps/core.xml'

class OpenXmlParser(BaseParser):
    @staticmethod
    def supported_mimes() -> List[str]:
        return ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
        # TODO add all supported types OR simpe refex with application/vnd.openxmlformats.*

    def __init__(self) -> None:
        super().__init__()
        self.__et = None
        self.__path = None

    def parse(self, filename: str) -> None:
        zf = zipfile.ZipFile(filename)
        self.__et = xml.etree.ElementTree.fromstring(zf.read(XML_LOCATION))
        self.__path = filename

    def get_fields(self) -> List[str]:
        return [
            FIELD_COREPROPERTIES,
            FIELD_TITLE,
            FIELD_SUBJECT,
            FIELD_CREATOR,
            FIELD_KEYWORDS,
            FIELD_DESCRIPTION,
            FIELD_LASTMODIFIEDBY,
            FIELD_REVISION,
            FIELD_CREATED,
            FIELD_MODIFIED,
        ]

    def set_field(self, field: str, value: Optional[str]) -> None:
        for elem in self.__et.iter():
            if elem.tag is field:
                elem.text = value

    def clear(self):
        for elem in self.__et.iter():
            elem.text = ""

    def delete_field(self, field: str) -> None:
        for elem in self.__et.iter():
            if elem.tag is field:
                elem.text = ""

    def get_all_values(self) -> Dict[str, str]:
        values = {}
        for elem in self.__et.iter():
            values[elem.tag] = elem.text
        return values

    def write(self) -> None:
        xml_string = xml.etree.ElementTree.tostring(self.__et, encoding='utf8', method='xml')
        with zipfile.ZipFile(self.__path, 'w') as myzip:
            myzip.writestr(XML_LOCATION, data=xml_string)
        # TODO fix saving to .docx instead of zip

from typing import Dict, List, Optional

import re  # type: ignore
import shutil  # type: ignore
import zipfile  # type: ignore
import tempfile  # type: ignore
import xml.etree.ElementTree  # type: ignore

from .base import BaseParser

FIELD_CORE_PROPERTIES = "coreProperties"
FIELD_TITLE = "title"
FIELD_SUBJECT = "subject"
FIELD_CREATOR = "creator"
FIELD_KEYWORDS = "keywords"
FIELD_DESCRIPTION = "description"
FIELD_LASTMODIFIEDBY = "lastModifiedBy"
FIELD_REVISION = "revision"
FIELD_CREATED = "created"
FIELD_MODIFIED = "modified"

XML_LOCATION = "docProps/core.xml"
XML_DECLARATION = "<?xml version='1.0' encoding='UTF-8' standalone='yes'?>"
NAMESPACES = {
    "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcmitype": "http://purl.org/dc/dcmitype/",
    "dcterms": "http://purl.org/dc/terms/",
    "dcmitype": "http://purl.org/dc/dcmitype/",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}


class OpenXmlParser(BaseParser):
    @staticmethod
    def supported_mimes() -> List[str]:
        return [
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # docx
            "application/vnd.openxmlformats-officedocument.wordprocessingml.template",  # dotx
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # xlsx
            "application/vnd.openxmlformats-officedocument.spreadsheetml.template",  # xltx
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",  # pptx
            "application/vnd.openxmlformats-officedocument.presentationml.template",  # potx
            "application/vnd.openxmlformats-officedocument.presentationml.slideshow",  # ppsx
        ]

    def __init__(self) -> None:
        super().__init__()
        self.__tree: xml.etree.ElementTree.Element
        self.__path: str

    def parse(self, filename: str) -> None:
        xml_string = zipfile.ZipFile(filename).read(XML_LOCATION)
        self.__tree = xml.etree.ElementTree.fromstring(xml_string)
        self.__path = filename
        for key, value in NAMESPACES.items():
            xml.etree.ElementTree.register_namespace(key, value)

    def get_fields(self) -> List[str]:
        return [
            FIELD_CORE_PROPERTIES,
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
        super().set_field(field, value)
        for elem in self.__tree.iter():
            if elem.tag.endswith(
                field
            ):  # real tags are more complex - eg. '{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}coreProperties' so we check only end
                elem.text = value

    def clear(self):
        for elem in self.__tree.iter():
            elem.text = ""

    def delete_field(self, field: str) -> None:
        super().delete_field(field)
        for elem in self.__tree.iter():
            if elem.tag.endswith(field):
                elem.text = ""

    def get_all_values(self) -> Dict[str, str]:
        values = {}
        pattern = re.compile("({.*})(.*)")
        for elem in self.__tree.iter():
            if elem.text and pattern.match(elem.tag):
                key = pattern.search(elem.tag).group(2)  # type: ignore
                values[key] = elem.text
        return values

    def write(self) -> None:
        xmlString = xml.etree.ElementTree.tostring(self.__tree).decode("utf-8")
        xmlString = XML_DECLARATION + xmlString

        temp = tempfile.NamedTemporaryFile()
        shutil.copyfile(self.__path, temp.name)

        with zipfile.ZipFile(temp) as inZip, zipfile.ZipFile(
            self.__path, "w"
        ) as outZip:
            for inZipInfo in inZip.infolist():
                with inZip.open(inZipInfo) as infile:
                    if inZipInfo.filename == XML_LOCATION:
                        content = xmlString
                        outZip.writestr(inZipInfo.filename, content)
                    else:
                        content = infile.read().decode("utf-8")
                        outZip.writestr(inZipInfo.filename, content)

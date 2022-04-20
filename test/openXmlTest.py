import os
import sys
import unittest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


from src.modules.openXml import OpenXmlParser

TEST_FIELD = "title"
TEST_STRING = "TEST"
RESOURCE_FILE = "/resources/test.docx"


class OpenXmlTest(unittest.TestCase):
    __parser: OpenXmlParser
    __file_path : str

    def setUp(self):
        self.__file_path = SCRIPT_DIR + RESOURCE_FILE
        self.__parser = OpenXmlParser()
        self.__parser.parse(self.__file_path)

    def test_parser(self):
        self.assertIsNotNone(self.__parser)
        self.assertTrue(isinstance(self.__parser, OpenXmlParser))

    def test_fields(self):
        fields = self.__parser.get_fields()
        expected_fields = ['coreProperties', 'title', 'subject', 'creator', 'keywords', 'description',
                            'lastModifiedBy', 'revision', 'created', 'modified']
        self.assertEqual(fields, expected_fields)

    def test_set_field(self):
        self.__parser.set_field(TEST_FIELD, TEST_STRING)
        all_values = self.__parser.get_all_values()
        self.assertEqual(all_values[TEST_FIELD], TEST_STRING)

    # def test_delete_field(self):


if __name__ == '__main__':
    unittest.main()

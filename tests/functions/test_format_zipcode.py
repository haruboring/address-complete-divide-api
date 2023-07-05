from unittest import TestCase
from unittest.mock import MagicMock, patch

from requests import Response

from src.functions.format_zipcode import format_zipcode


class TestFormatZipcode(TestCase):
    def test_format_zipcode_unchange(self):
        self.assertEqual(format_zipcode("1000000"), "1000000")
        self.assertEqual(format_zipcode(""), "")
        self.assertEqual(format_zipcode("10000000000"), "10000000000")

    def test_format_zipcode_full_number(self):
        self.assertEqual(format_zipcode("１００００００"), "1000000")

    def test_format_zipcode_delete_hyphen(self):
        self.assertEqual(format_zipcode("100-0000"), "1000000")

    def test_format_zipcode(self):
        self.assertEqual(format_zipcode("１００−００００"), "1000000")
        self.assertEqual(format_zipcode("-vdfs０２＝＝０ー"), "020")

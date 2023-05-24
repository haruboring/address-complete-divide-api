from unittest import TestCase
from unittest.mock import MagicMock, patch

from pydantic import BaseModel, Field
from requests import Response

from src.interfaces.address import Address


class TestAddressInfo(TestCase):
    def setUp(self):
        self.address = Address()

    def test_complete_address(self):
        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 200
        response_mock.json.return_value = {"results": [{"address1": "東京都", "address2": "港区", "address3": "芝公園"}]}

        with patch("requests.get", return_value=response_mock):
            self.address.zipcode = ""
            self.address.complete_address()

        self.assertEqual(self.address.completed_prefecture, "東京都")
        self.assertEqual(self.address.completed_city, "港区")
        self.assertEqual(self.address.completed_town, "芝公園")

    def test_normalize_address(self):
        self.address.address = "東京都　港区１−１−１東京スカイツリー１０１"
        self.address.normalize_address()

        self.assertEqual(self.address.rest_address, "東京都港区1-1-1東京スカイツリー101")

    def test_divide_address(self):
        self.address.rest_address = "東京都港区1-1-1東京スカイツリー101"
        self.address.divide_address()

        self.assertEqual(self.address.prefecture, "東京都")
        self.assertEqual(self.address.city, "港区")
        self.assertEqual(self.address.town, "")
        self.assertEqual(self.address.house_number, "1-1-1")
        self.assertEqual(self.address.building_name, "東京スカイツリー")
        self.assertEqual(self.address.room_number, "101")

    def test_delete_extra_attributes(self):
        self.address.zipcode = "100-0000"
        self.address.address = "東京都港区芝公園1-1東京スカイツリー101"
        self.address.is_completed = False
        self.address.completed_prefecture = "東京都"
        self.address.completed_city = "港区"
        self.address.completed_town = "芝公園"
        self.address.rest_address = "1-1-1東京スカイツリー101"

        self.address.delete_extra_attributes()

        with self.assertRaises(AttributeError):
            _ = self.address.zipcode

        with self.assertRaises(AttributeError):
            _ = self.address.address

        with self.assertRaises(AttributeError):
            _ = self.address.is_completed

        with self.assertRaises(AttributeError):
            _ = self.address.completed_prefecture

        with self.assertRaises(AttributeError):
            _ = self.address.completed_city

        with self.assertRaises(AttributeError):
            _ = self.address.completed_town

        with self.assertRaises(AttributeError):
            _ = self.address.rest_address

    def test_get_completed_address_count(self):
        self.address.is_completed = True

        count = self.address.get_completed_address_count(0)
        self.assertEqual(count, 1)

        self.address.is_completed = False

        count = self.address.get_completed_address_count(0)
        self.assertEqual(count, 0)

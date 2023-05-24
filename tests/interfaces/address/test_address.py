from unittest import TestCase
from unittest.mock import MagicMock, patch

from requests import Response

from src.interfaces.address import AddressInfo


class TestAddressInfoInfo(TestCase):
    def setUp(self):
        self.address_info = AddressInfo()

    def test_complete_address_successfully1(self):
        self.address_info.zipcode = "1050011"
        self.address_info.complete_address()

        self.assertEqual(self.address_info.completed_prefecture, "東京都")
        self.assertEqual(self.address_info.completed_city, "港区")
        self.assertEqual(self.address_info.completed_town, "芝公園")

    def test_complete_address_successfully2(self):
        self.address_info.zipcode = "105-0011"
        self.address_info.complete_address()

        self.assertEqual(self.address_info.completed_prefecture, "東京都")
        self.assertEqual(self.address_info.completed_city, "港区")
        self.assertEqual(self.address_info.completed_town, "芝公園")

    def test_complete_address_failed(self):
        self.address_info.zipcode = "999-9999"
        self.address_info.complete_address()

        self.assertEqual(self.address_info.completed_prefecture, "")
        self.assertEqual(self.address_info.completed_city, "")
        self.assertEqual(self.address_info.completed_town, "")

    def test_normalize_address(self):
        self.address_info.address = "東京都　港区１−１−１東京スカイツリー１０１"
        self.address_info.normalize_address()

        self.assertEqual(self.address_info.rest_address, "東京都港区1-1-1東京スカイツリー101")

    def test_divide_address(self):
        self.address_info.rest_address = "東京都港区1-1-1東京スカイツリー101"
        self.address_info.divide_address()

        self.assertEqual(self.address_info.prefecture, "東京都")
        self.assertEqual(self.address_info.city, "港区")
        self.assertEqual(self.address_info.town, "")
        self.assertEqual(self.address_info.house_number, "1-1-1")
        self.assertEqual(self.address_info.building_name, "東京スカイツリー")
        self.assertEqual(self.address_info.room_number, "101")

    def test_delete_extra_attributes(self):
        self.address_info.zipcode = "105-0011"
        self.address_info.address = "東京都港区芝公園1-1東京スカイツリー101"
        self.address_info.is_completed = False
        self.address_info.completed_prefecture = "東京都"
        self.address_info.completed_city = "港区"
        self.address_info.completed_town = "芝公園"
        self.address_info.rest_address = "1-1-1東京スカイツリー101"

        self.address_info.delete_extra_attributes()

        with self.assertRaises(AttributeError):
            _ = self.address_info.zipcode

        with self.assertRaises(AttributeError):
            _ = self.address_info.address

        with self.assertRaises(AttributeError):
            _ = self.address_info.is_completed

        with self.assertRaises(AttributeError):
            _ = self.address_info.completed_prefecture

        with self.assertRaises(AttributeError):
            _ = self.address_info.completed_city

        with self.assertRaises(AttributeError):
            _ = self.address_info.completed_town

        with self.assertRaises(AttributeError):
            _ = self.address_info.rest_address

    def test_get_completed_address_count1(self):
        self.address_info.is_completed = True

        count = self.address_info.get_completed_address_count(0)
        self.assertEqual(count, 1)

    def test_get_completed_address_count2(self):
        self.address_info.is_completed = False

        count = self.address_info.get_completed_address_count(0)
        self.assertEqual(count, 0)

from unittest import TestCase
from unittest.mock import MagicMock, patch

from requests import Response

from src.interfaces.address import Address


class TestAddressInfo(TestCase):
    def setUp(self):
        self.address = Address()

    def test_complete_address_successfully1(self):
        self.address.zipcode = "1050011"
        self.address.complete_address()

        self.assertEqual(self.address.completed_prefecture, "東京都")
        self.assertEqual(self.address.completed_city, "港区")
        self.assertEqual(self.address.completed_town, "芝公園")

    def test_complete_address_successfully2(self):
        self.address.zipcode = "105-0011"
        self.address.complete_address()

        self.assertEqual(self.address.completed_prefecture, "東京都")
        self.assertEqual(self.address.completed_city, "港区")
        self.assertEqual(self.address.completed_town, "芝公園")

    def test_complete_address_failed(self):
        self.address.zipcode = "999-9999"
        self.address.complete_address()

        self.assertEqual(self.address.completed_prefecture, "")
        self.assertEqual(self.address.completed_city, "")
        self.assertEqual(self.address.completed_town, "")

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
        self.address.zipcode = "105-0011"
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

    def test_get_completed_address_count1(self):
        self.address.is_completed = True

        count = self.address.get_completed_address_count(0)
        self.assertEqual(count, 1)

    def test_get_completed_address_count2(self):
        self.address.is_completed = False

        count = self.address.get_completed_address_count(0)
        self.assertEqual(count, 0)

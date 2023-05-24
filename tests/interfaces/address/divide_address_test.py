from unittest import TestCase

from src.interfaces.address import Address


class TestDivideAddress(TestCase):
    def test_divide_address_without_complete(self):
        completed_count: int = 0
        self.address = Address(address="東京都港区芝公園４丁目２−８", zipcode="")

        self.address.complete_address()
        self.address.normalize_address()

        self.assertEqual(self.address.rest_address, "東京都港区芝公園4/tyoume2-8")

        self.address.divide_address()
        completed_count = self.address.get_completed_address_count(completed_count)

        self.assertEqual(self.address.is_completed, False)
        self.assertEqual(self.address.prefecture, "東京都")
        self.assertEqual(self.address.city, "港区")
        self.assertEqual(self.address.town, "芝公園")
        self.assertEqual(self.address.house_number, "4-2-8")
        self.assertEqual(self.address.building_name, "")
        self.assertEqual(self.address.room_number, "")
        self.assertEqual(completed_count, 0)

    def test_divide_address_with_complete(self):
        completed_count: int = 0
        self.address = Address(address="芝公園４丁目２−８", zipcode="105-0011")

        self.address.complete_address()
        self.address.normalize_address()

        self.assertEqual(self.address.rest_address, "芝公園4/tyoume2-8")

        self.address.divide_address()
        completed_count = self.address.get_completed_address_count(completed_count)

        self.assertEqual(self.address.is_completed, True)
        self.assertEqual(self.address.prefecture, "東京都")
        self.assertEqual(self.address.city, "港区")
        self.assertEqual(self.address.town, "芝公園")
        self.assertEqual(self.address.house_number, "4-2-8")
        self.assertEqual(self.address.building_name, "")
        self.assertEqual(self.address.room_number, "")
        self.assertEqual(completed_count, 1)

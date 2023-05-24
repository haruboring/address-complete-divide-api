from unittest import TestCase

from src.interfaces.address import AddressInfo


class TestDivideAddressInfo(TestCase):
    def test_divide_address_without_complete(self):
        completed_count: int = 0
        self.address_info = AddressInfo(address="東京都港区芝公園４丁目２−８", zipcode="")

        self.address_info.complete_address()
        self.address_info.normalize_address()

        self.assertEqual(self.address_info.rest_address, "東京都港区芝公園4/tyoume2-8")

        self.address_info.divide_address()
        completed_count = self.address_info.get_completed_address_count(completed_count)

        self.assertEqual(self.address_info.is_completed, False)
        self.assertEqual(self.address_info.prefecture, "東京都")
        self.assertEqual(self.address_info.city, "港区")
        self.assertEqual(self.address_info.town, "芝公園")
        self.assertEqual(self.address_info.house_number, "4-2-8")
        self.assertEqual(self.address_info.building_name, "")
        self.assertEqual(self.address_info.room_number, "")
        self.assertEqual(completed_count, 0)

    def test_divide_address_with_complete(self):
        completed_count: int = 0
        self.address_info = AddressInfo(address="芝公園４丁目２−８", zipcode="105-0011")

        self.address_info.complete_address()
        self.address_info.normalize_address()

        self.assertEqual(self.address_info.rest_address, "芝公園4/tyoume2-8")

        self.address_info.divide_address()
        completed_count = self.address_info.get_completed_address_count(completed_count)

        self.assertEqual(self.address_info.is_completed, True)
        self.assertEqual(self.address_info.prefecture, "東京都")
        self.assertEqual(self.address_info.city, "港区")
        self.assertEqual(self.address_info.town, "芝公園")
        self.assertEqual(self.address_info.house_number, "4-2-8")
        self.assertEqual(self.address_info.building_name, "")
        self.assertEqual(self.address_info.room_number, "")
        self.assertEqual(completed_count, 1)

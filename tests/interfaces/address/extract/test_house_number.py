from unittest import TestCase

from src.interfaces.address import AddressInfo


class TestExtractHouseNumber(TestCase):
    def set_address_info(self, rest_address: str) -> None:
        self.address_info = AddressInfo()
        self.address_info.rest_address = rest_address

    def test_extract_house_number1(self) -> None:
        self.set_address_info("1/tyoume二-3山田ハウス")
        self.assertEqual(self.address_info.extract_house_number(), ("1-2-3", "山田ハウス"))

    def test_extract_house_number2(self) -> None:
        self.set_address_info("1-3-1/gou")
        self.assertEqual(self.address_info.extract_house_number(), ("1-3-1", ""))

    def test_extract_house_number3(self) -> None:
        self.set_address_info("1/no3/no2")
        self.assertEqual(self.address_info.extract_house_number(), ("1-3-2", ""))

    def test_extract_house_number4(self) -> None:
        self.set_address_info("山田ハウス")
        self.assertEqual(self.address_info.extract_house_number(), ("", "山田ハウス"))

    def test_extract_house_number_with_more_4_number1(self) -> None:
        self.set_address_info("1-3-1-302")
        self.assertEqual(self.address_info.extract_house_number(), ("1-3-1", "302"))

    def test_extract_house_number_with_more_4_number2(self) -> None:
        self.set_address_info("1-2-3-4-5")
        self.assertEqual(self.address_info.extract_house_number(), ("1-2-3", "4-5"))

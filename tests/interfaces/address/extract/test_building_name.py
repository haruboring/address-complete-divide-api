from unittest import TestCase

from src.interfaces.address import Address


class TestExtractBuildingName(TestCase):
    def set_address(self, rest_address: str) -> None:
        self.address = Address()
        self.address.rest_address = rest_address

    def test_extract_building_name1(self) -> None:
        self.set_address("山田ハウス321/gou室")
        self.assertEqual(self.address.extract_building_name(), ("山田ハウス", "321/gou室"))

    def test_extract_building_name2(self) -> None:
        self.set_address("山田ハウス")
        self.assertEqual(self.address.extract_building_name(), ("山田ハウス", ""))

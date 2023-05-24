from unittest import TestCase

from src.interfaces.address import AddressInfo


class TestExtractRoomNumber(TestCase):
    def set_address_info(self, rest_address: str) -> None:
        self.address_info = AddressInfo()
        self.address_info.rest_address = rest_address

    def test_extract_room_number1(self) -> None:
        self.set_address_info("321/gou室")
        self.assertEqual(self.address_info.extract_room_number(), "321号室")

    def test_extract_room_number2(self) -> None:
        self.set_address_info("321")
        self.assertEqual(self.address_info.extract_room_number(), "321")

    def test_extract_room_number3(self) -> None:
        self.set_address_info("")
        self.assertEqual(self.address_info.extract_room_number(), "")

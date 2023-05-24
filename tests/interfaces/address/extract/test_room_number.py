from unittest import TestCase

from src.interfaces.address import Address


class TestExtractRoomNumber(TestCase):
    def set_address(self, rest_address: str) -> None:
        self.address = Address()
        self.address.rest_address = rest_address

    def test_extract_room_number1(self) -> None:
        self.set_address("321/gou室")
        self.assertEqual(self.address.extract_room_number(), "321号室")

    def test_extract_room_number2(self) -> None:
        self.set_address("321")
        self.assertEqual(self.address.extract_room_number(), "321")

    def test_extract_room_number3(self) -> None:
        self.set_address("")
        self.assertEqual(self.address.extract_room_number(), "")

from unittest import TestCase

from src.interfaces.address import Address


class TestExtractPrefecture(TestCase):
    def set_address(self, rest_address: str, completed_prefecture: str) -> None:
        self.address = Address()
        self.address.rest_address = rest_address
        self.address.completed_prefecture = completed_prefecture

    def test_extract_prefecture_without_complete1(self) -> None:
        self.set_address("東京都大田区〇〇", "")
        self.assertEqual(self.address.extract_prefecture(), ("東京都", "大田区〇〇"))
        self.assertEqual(self.address.is_completed, False)

    def test_extract_prefecture_without_complete2(self) -> None:
        self.set_address("愛媛県〇〇", "")
        self.assertEqual(self.address.extract_prefecture(), ("愛媛県", "〇〇"))
        self.assertEqual(self.address.is_completed, False)

    def test_extract_prefecture_with_complete1(self) -> None:
        self.set_address("東京都大田区〇〇", "神奈川県")
        self.assertEqual(self.address.extract_prefecture(), ("東京都", "大田区〇〇"))
        self.assertEqual(self.address.is_completed, False)

    def test_extract_prefecture_with_complete2(self) -> None:
        self.set_address("松山市〇〇", "愛媛県")
        self.assertEqual(self.address.extract_prefecture(), ("愛媛県", "松山市〇〇"))
        self.assertEqual(self.address.is_completed, True)

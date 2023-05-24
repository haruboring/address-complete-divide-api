from unittest import TestCase

from src.interfaces.address import AddressInfo


class TestExtractPrefecture(TestCase):
    def set_address_info(self, rest_address: str, completed_prefecture: str) -> None:
        self.address_info = AddressInfo()
        self.address_info.rest_address = rest_address
        self.address_info.completed_prefecture = completed_prefecture

    def test_extract_prefecture_without_complete1(self) -> None:
        self.set_address_info("東京都大田区〇〇", "")
        self.assertEqual(self.address_info.extract_prefecture(), ("東京都", "大田区〇〇"))
        self.assertEqual(self.address_info.is_completed, False)

    def test_extract_prefecture_without_complete2(self) -> None:
        self.set_address_info("愛媛県〇〇", "")
        self.assertEqual(self.address_info.extract_prefecture(), ("愛媛県", "〇〇"))
        self.assertEqual(self.address_info.is_completed, False)

    def test_extract_prefecture_with_complete1(self) -> None:
        self.set_address_info("東京都大田区〇〇", "神奈川県")
        self.assertEqual(self.address_info.extract_prefecture(), ("東京都", "大田区〇〇"))
        self.assertEqual(self.address_info.is_completed, False)

    def test_extract_prefecture_with_complete2(self) -> None:
        self.set_address_info("松山市〇〇", "愛媛県")
        self.assertEqual(self.address_info.extract_prefecture(), ("愛媛県", "松山市〇〇"))
        self.assertEqual(self.address_info.is_completed, True)

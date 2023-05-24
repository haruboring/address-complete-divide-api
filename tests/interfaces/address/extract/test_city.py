from unittest import TestCase

from src.interfaces.address import AddressInfo


class TestExtractCity(TestCase):
    def set_address_info(self, rest_address: str, completed_city: str) -> None:
        self.address_info = AddressInfo()
        self.address_info.rest_address = rest_address
        self.address_info.completed_city = completed_city

    def test_extract_city_without_complete1(self) -> None:
        self.set_address_info("大田区北千束○-○-○", "")
        self.assertEqual(self.address_info.extract_city(), ("大田区", "北千束○-○-○"))
        self.assertEqual(self.address_info.is_completed, False)

    def test_extract_city_without_complete2(self) -> None:
        self.set_address_info("廿日市市下平良○-○-○", "")
        self.assertEqual(self.address_info.extract_city(), ("廿日市市", "下平良○-○-○"))
        self.assertEqual(self.address_info.is_completed, False)

    def test_extract_city_without_complete3(self) -> None:
        self.set_address_info("伊予市双海町○-○-○", "")
        self.assertEqual(self.address_info.extract_city(), ("伊予市", "双海町○-○-○"))
        self.assertEqual(self.address_info.is_completed, False)

    def test_extract_city_without_complete4(self) -> None:
        self.set_address_info("野々市市三納1丁目1番地", "")
        self.assertEqual(self.address_info.extract_city(), ("野々市市", "三納1丁目1番地"))
        self.assertEqual(self.address_info.is_completed, False)

    def test_extract_city_without_complete5(self) -> None:
        self.set_address_info("松山市市坪西町", "")
        self.assertEqual(self.address_info.extract_city(), ("松山市", "市坪西町"))
        self.assertEqual(self.address_info.is_completed, False)

    def test_extract_city_without_complete6(self) -> None:
        self.set_address_info("町○○市××", "")
        self.assertEqual(self.address_info.extract_city(), ("町○○市", "××"))
        self.assertEqual(self.address_info.is_completed, False)

    def test_extract_city_without_complete7(self) -> None:
        self.set_address_info("三区町××", "")
        self.assertEqual(self.address_info.extract_city(), ("三区町", "××"))
        self.assertEqual(self.address_info.is_completed, False)

    def test_extract_city_without_complete8(self) -> None:
        self.set_address_info("千代田区××", "")
        self.assertEqual(self.address_info.extract_city(), ("千代田区", "××"))
        self.assertEqual(self.address_info.is_completed, False)

    def test_extract_city_with_complete1(self) -> None:
        self.set_address_info("目黒区", "目黒区")
        self.assertEqual(self.address_info.extract_city(), ("目黒区", ""))
        self.assertEqual(self.address_info.is_completed, False)

    def test_extract_city_with_complete2(self) -> None:
        self.set_address_info("", "目黒区")
        self.assertEqual(self.address_info.extract_city(), ("目黒区", ""))
        self.assertEqual(self.address_info.is_completed, True)

    def test_extract_city_with_complete3(self) -> None:
        self.set_address_info("大岡山", "目黒区")
        self.assertEqual(self.address_info.extract_city(), ("目黒区", "大岡山"))
        self.assertEqual(self.address_info.is_completed, True)

    def test_extract_city_with_complete4(self) -> None:
        self.set_address_info("目黒区大岡山", "足立区")
        self.assertEqual(self.address_info.extract_city(), ("目黒区", "大岡山"))
        self.assertEqual(self.address_info.is_completed, False)

from unittest import TestCase

from src.interfaces.address import AddressInfo


class TestExtractTown(TestCase):
    def set_address_info(self, rest_address: str, completed_town: str) -> None:
        self.address_info = AddressInfo()
        self.address_info.rest_address = rest_address
        self.address_info.completed_town = completed_town

    def test_extract_town_without_complete1(self) -> None:
        self.set_address_info("北千束1-1-1〇〇", "")
        self.assertEqual(self.address_info.extract_town(), ("北千束", "1-1-1〇〇"))
        self.assertEqual(self.address_info.is_completed, False)

    def test_extract_town_without_complete2(self) -> None:
        self.set_address_info("一/ban町1", "")
        self.assertEqual(self.address_info.extract_town(), ("一番町", "1"))
        self.assertEqual(self.address_info.is_completed, False)

    def test_extract_town_without_complete3(self) -> None:
        self.set_address_info("北千束1〇〇", "")
        self.assertEqual(self.address_info.extract_town(), ("北千束", "1〇〇"))
        self.assertEqual(self.address_info.is_completed, False)

    def test_extract_town_without_complete4(self) -> None:
        self.set_address_info("一/ban町1/tyoume", "")
        self.assertEqual(self.address_info.extract_town(), ("一番町", "1/tyoume"))
        self.assertEqual(self.address_info.is_completed, False)

    def test_extract_town_without_complete5(self) -> None:
        self.set_address_info("1-1-1", "")
        self.assertEqual(self.address_info.extract_town(), ("", "1-1-1"))
        self.assertEqual(self.address_info.is_completed, False)

    def test_extract_town_with_complete1(self) -> None:
        self.set_address_info("北千束1-1-1〇〇", "北千束")
        self.assertEqual(self.address_info.extract_town(), ("北千束", "1-1-1〇〇"))
        self.assertEqual(self.address_info.is_completed, False)

    def test_extract_town_with_complete2(self) -> None:
        self.set_address_info("一/ban町1", "三番町")
        self.assertEqual(self.address_info.extract_town(), ("一番町", "1"))
        self.assertEqual(self.address_info.is_completed, False)

    def test_extract_town_with_complete3(self) -> None:
        self.set_address_info("", "北千束")
        self.assertEqual(self.address_info.extract_town(), ("北千束", ""))
        self.assertEqual(self.address_info.is_completed, True)

    def test_extract_town_with_complete4(self) -> None:
        self.set_address_info("山1-1-1", "海")
        self.assertEqual(self.address_info.extract_town(), ("山", "1-1-1"))
        self.assertEqual(self.address_info.is_completed, False)

    def test_extract_town_with_complete5(self) -> None:
        self.set_address_info("1-1-1", "北千束")
        self.assertEqual(self.address_info.extract_town(), ("北千束", "1-1-1"))
        self.assertEqual(self.address_info.is_completed, True)

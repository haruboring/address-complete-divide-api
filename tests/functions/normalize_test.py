from unittest import TestCase

from src.functions.normalize import Normalize  # type: ignore


class TestConvertFullWidthDigitToHalfWidthDigit(TestCase):
    def test_convert_full_width_digit_to_half_width_digit1(self) -> None:
        return_value = Normalize.convert_full_width_digit_to_half_width_digit("２００１年生まれ")
        self.assertEqual(return_value, "2001年生まれ")

    def test_convert_full_width_digit_to_half_width_digit2(self) -> None:
        return_value = Normalize.convert_full_width_digit_to_half_width_digit("お酒は２０歳になってから")
        self.assertEqual(return_value, "お酒は20歳になってから")


class TestConvertChineseNumeralToHalfWidthDigit(TestCase):
    def test_convert_Chinese_numeral_to_half_width_digit1(self) -> None:
        return_value = Normalize.convert_Chinese_numeral_to_half_width_digit("一二三四五")
        self.assertEqual(return_value, "12345")

    def test_convert_Chinese_numeral_to_half_width_digit2(self) -> None:
        return_value = Normalize.convert_Chinese_numeral_to_half_width_digit("一に曰わく、和を以て貴しとなし、さからうことなきを宗とせよ。")
        self.assertEqual(return_value, "1に曰わく、和を以て貴しとなし、さからうことなきを宗とせよ。")


class TestConvertMacronToHyphen(TestCase):
    def test_convert_macron_to_hyphen1(self) -> None:
        return_value = Normalize.convert_macron_to_hyphen("1ー2")
        self.assertEqual(return_value, "1-2")

    def test_convert_macron_to_hyphen2(self) -> None:
        return_value = Normalize.convert_macron_to_hyphen("1ー2ー3-4")
        self.assertEqual(return_value, "1-2-3-4")

    def test_convert_macron_to_hyphen3(self) -> None:
        return_value = Normalize.convert_macron_to_hyphen("1−2−3−4")
        self.assertEqual(return_value, "1-2-3-4")


class TestConvertHouseNumberExpressionToHyphen(TestCase):
    def test_convert_house_number_expression_to_hyphen1(self) -> None:
        return_value = Normalize.convert_house_number_expression_to_hyphen("1/tyoume5/banti3/gou")
        self.assertEqual(return_value, "1-5-3-")

    def test_convert_house_number_expression_to_hyphen2(self) -> None:
        return_value = Normalize.convert_house_number_expression_to_hyphen("5-321/ban")
        self.assertEqual(return_value, "5-321-")


class TestFillSpace(TestCase):
    def test_fill_space1(self) -> None:
        return_value = Normalize.fill_space("あ い　う  え　　お")
        self.assertEqual(return_value, "あいうえお")

    def test_fill_space2(self) -> None:
        return_value = Normalize.fill_space("   ")
        self.assertEqual(return_value, "")


class TestReverseHouseNumberExpression(TestCase):
    def test_reverse_house_number_expression1(self) -> None:
        return_value = Normalize.reverse_house_number_expression("302/gou室")
        self.assertEqual(return_value, "302号室")

    def test_reverse_house_number_expression2(self) -> None:
        return_value = Normalize.reverse_house_number_expression("松山一/ban町校")
        self.assertEqual(return_value, "松山一番町校")


class TestReplaceHouseNumberExpression(TestCase):
    def test_replace_house_number_expression1(self) -> None:
        return_value = Normalize.replace_house_number_expression("愛媛県松番市一番町3丁目3-6")
        self.assertEqual(return_value, "愛媛県松/ban市一/ban町3/tyoume3-6")

    def test_replace_house_number_expression2(self) -> None:
        return_value = Normalize.replace_house_number_expression("番地番番番地号の号丁目")
        self.assertEqual(return_value, "/banti/ban/ban/banti/gou/no/gou/tyoume")

    def test_replace_house_number_expression3(self) -> None:
        return_value = Normalize.replace_house_number_expression("三丁目")
        self.assertEqual(return_value, "3/tyoume")

import re


class Normalize:
    @staticmethod
    def convert_full_width_digit_to_half_width_digit(string: str) -> str:
        """
        args: address_data: str (example: 東京都港区元麻布1-６-9)
        return: formatted_address_data: str (example: 東京都港区元麻布1-6-9)
        """

        MAPPING_DICTIONARY: dict[str, str] = {
            "１": "1",
            "２": "2",
            "３": "3",
            "４": "4",
            "５": "5",
            "６": "6",
            "７": "7",
            "８": "8",
            "９": "9",
            "０": "0",
        }

        formatted_string: str = ""

        for character in string:
            if character in MAPPING_DICTIONARY.keys():
                formatted_string += MAPPING_DICTIONARY[character]
            else:
                formatted_string += character

        return formatted_string

    @staticmethod
    def convert_Chinese_numeral_to_half_width_digit(string: str) -> str:
        """
        args: address_data: str (example: 東京都港区元麻布1-六-9)
        return: formatted_address_data: str (example: 東京都港区元麻布1-6-9)
        """

        MAPPING_DICTIONARY: dict[str, str] = {
            "一": "1",
            "二": "2",
            "三": "3",
            "四": "4",
            "五": "5",
            "六": "6",
            "七": "7",
            "八": "8",
            "九": "9",
            "〇": "0",
        }

        formatted_string: str = ""

        for character in string:
            if character in MAPPING_DICTIONARY.keys():
                formatted_string += MAPPING_DICTIONARY[character]
            else:
                formatted_string += character

        return formatted_string

    @staticmethod
    def convert_macron_to_hyphen(address: str) -> str:
        formatted_address: str = address

        # 1ー43のような形は一つ目が番地と考えられるのでsearchでいい
        match = re.search("([0-9]+ー)+[0-9]+", address)
        if match is not None:
            matched_string: str = match.group()
            formatted_string: str = matched_string.replace("ー", "-")
            formatted_address = address.replace(matched_string, formatted_string, 1)

        return formatted_address

    @staticmethod
    def convert_house_number_expression_to_hyphen(address: str) -> str:
        address = address.replace("/tyoume", "-")
        address = address.replace("/banti", "-")
        address = address.replace("/ban", "-")
        address = address.replace("/gou", "-")
        formatted_address: str = address.replace("/no", "-")

        return formatted_address

    @staticmethod
    def fill_space(address: str) -> str:
        address = address.replace(" ", "")
        address = address.replace("　", "")
        formatted_address: str = address.replace("　", "")

        return formatted_address

    @staticmethod
    def reverse_house_number_expression(address: str) -> str:
        address = address.replace("/tyoume", "丁目")
        address = address.replace("/banti", "番地")
        address = address.replace("/ban", "番")
        address = address.replace("/gou", "号")
        formatted_address: str = address.replace("/no", "の")

        return formatted_address

    @classmethod
    def replace_house_number_expression(cls, address: str) -> str:
        address = address.replace("丁目", "/tyoume")
        address = address.replace("番地", "/banti")
        address = address.replace("番", "/ban")
        address = address.replace("号", "/gou")
        formatted_address: str = address.replace("の", "/no")

        match = re.search("[〇-九]+/tyoume", address)
        if match is not None:
            matched_string: str = match.group()
            formatted_string = cls.convert_Chinese_numeral_to_half_width_digit(matched_string)
            formatted_address = formatted_address.replace(matched_string, formatted_string, 1)

        return formatted_address

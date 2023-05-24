import re

import requests
from pydantic import BaseModel, Field

from data.prefecture_names import PREFECTURE_NAMES
from data.special_city_names import SPECIAL_CITY_NAMES
from data.ward_names_of_tokyo import WARD_NAMES_OF_TOKYO
from src.functions.normalize import Normalize


class Address(BaseModel):
    zipcode: str = Field(default="", example="100-0000")
    address: str = Field(default="", example="東京都港区芝公園1-1東京スカイツリー101")

    # n個の住所が補完されましたというふうにしたい
    is_completed: bool = False
    completed_prefecture: str = ""
    completed_city: str = ""
    completed_town: str = ""

    rest_address: str = ""

    prefecture: str = ""
    city: str = ""
    town: str = ""
    house_number: str = ""
    building_name: str = ""
    room_number: str = ""

    def __str__(self) -> str:
        return f"都道府県:{self.prefecture}, 市区町村:{self.city}, 町域:{self.town}, 番地:{self.house_number}, 建物名:{self.building_name}, 部屋番号:{self.room_number}"

    def complete_address(self):
        url = f"https://zipcloud.ibsnet.co.jp/api/search?zipcode={self.zipcode}"
        response = requests.get(url)

        if response.status_code == 200 and response.json()["results"] is not None and len(response.json()["results"]) == 1:
            result = response.json()["results"][0]
            self.completed_prefecture = result.get("address1", "")
            self.completed_city = result.get("address2", "")
            self.completed_town = result.get("address3", "")

    def normalize_address(self):
        normalizing_address: str = self.address
        normalizing_address = Normalize.fill_space(normalizing_address)
        normalizing_address = Normalize.convert_full_width_digit_to_half_width_digit(normalizing_address)
        normalizing_address = Normalize.convert_macron_to_hyphen(normalizing_address)
        normalized_address: str = Normalize.replace_house_number_expression(normalizing_address)

        self.rest_address = normalized_address

    def divide_address(self):
        self.prefecture, self.rest_address = self.extract_prefecture()
        self.city, self.rest_address = self.extract_city()
        self.town, self.rest_address = self.extract_town()
        self.house_number, self.rest_address = self.extract_house_number()
        self.building_name, self.rest_address = self.extract_building_name()
        self.room_number = self.extract_room_number()

    def delete_extra_attributes(self):
        delattr(self, "zipcode")
        delattr(self, "address")
        delattr(self, "is_completed")
        delattr(self, "completed_prefecture")
        delattr(self, "completed_city")
        delattr(self, "completed_town")
        delattr(self, "rest_address")

    def get_completed_address_count(self, count: int) -> int:
        if self.is_completed:
            count += 1
        return count

    ####################################################################################################

    def extract_prefecture(self) -> tuple[str, str]:
        address: str = self.rest_address
        completed_prefecture: str = self.completed_prefecture

        for prefecture in PREFECTURE_NAMES:
            if re.match(prefecture, address) is not None:
                return prefecture, address.replace(prefecture, "", 1)

        # 県名が存在しない
        if completed_prefecture != "":
            self.is_completed = True
        return completed_prefecture, address

    def extract_city(self) -> tuple[str, str]:
        address: str = self.rest_address
        completed_city: str = self.completed_city

        # 郵便番号から求めた市区町村名と一致する場合
        if completed_city != "" and re.match(completed_city, address) is not None:
            return completed_city, address.replace(completed_city, "", 1)

        # 区で市区町村を区切るのは、東京23区のみ
        for ward_name in WARD_NAMES_OF_TOKYO:
            if re.match(ward_name, address) is not None:
                return ward_name, address.replace(ward_name, "", 1)

        # 分割ミスが発生する地名
        for special_city_name in SPECIAL_CITY_NAMES:
            if re.match(special_city_name, address) is not None:
                return special_city_name, address.replace(special_city_name, "", 1)

        # 市・町・村で分割する
        for special_pattern in ["市", "町", "村"]:
            match = re.search(".+?" + special_pattern, address)
            if match is not None:
                return Normalize.reverse_house_number_expression(match.group()), address.replace(match.group(), "", 1)

        # 市区町村が存在しない
        if completed_city != "":
            self.is_completed = True
        return completed_city, address

    def extract_town(self) -> tuple[str, str]:
        address: str = self.rest_address
        completed_town: str = self.completed_town

        # 郵便番号から求めた町域名と一致する場合
        if completed_town != "" and re.match(completed_town, address) is not None:
            return completed_town, address.replace(completed_town, "", 1)

        # 町域名が存在しない
        if completed_town != "" and address == "":
            self.is_completed = True
            return completed_town, ""

        if re.search("[0-9]+", address) is not None:
            town_and_rest_address: list[str] = re.split("[0-9]+", address, 1)
            town: str = town_and_rest_address[0]
            return Normalize.reverse_house_number_expression(town), address.replace(town, "", 1)

        else:
            return address, ""

    def extract_house_number(self) -> tuple[str, str]:
        address: str = self.rest_address
        match = re.match("[0-9〇一二三四五六七八九/tyoume/banti/ban/gou/no-]+", address)
        if match is not None:
            house_number: str = match.group()
            house_number = Normalize.convert_house_number_expression_to_hyphen(house_number)
            house_number = Normalize.convert_Chinese_numeral_to_half_width_digit(house_number)

            # 1-2-3-のようになっている場合がある
            if house_number[len(house_number) - 1] == "-":
                house_number = house_number[:-1]
            return house_number, address.replace(match.group(), "", 1)

        return "", address

    def extract_building_name(self) -> tuple[str, str]:
        address: str = self.rest_address
        building_name_and_rest_address: list[str] = re.split("[0-9]+", address, 1)
        building_name: str = building_name_and_rest_address[0]

        return Normalize.reverse_house_number_expression(building_name), address.replace(building_name, "", 1)

    def extract_room_number(self) -> str:
        address: str = self.rest_address

        return Normalize.reverse_house_number_expression(address)

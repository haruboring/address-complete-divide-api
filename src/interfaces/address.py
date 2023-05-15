import requests
from pydantic import BaseModel, Field


class Address(BaseModel):
    zipcode: str = Field(default="", example="100-0000")
    address: str = Field(default="", example="東京都港区芝公園1-1東京スカイツリー101")

    completed_prefecture: str = ""
    completed_city: str = ""
    completed_town: str = ""

    prefecture: str = ""
    city: str = ""
    town: str = ""
    house_number: str = ""
    building_name: str = ""
    room_number: str = ""

    def __str__(self) -> str:
        return f"郵便番号:{self.zipcode}, 住所:{self.address}"

    def complete_address(self):
        url = f"https://zipcloud.ibsnet.co.jp/api/search?zipcode={self.zipcode}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if data["results"]:
                result = data["results"][0]
                self.completed_prefecture = result.get("address1", "")
                self.completed_city = result.get("address2", "")
                self.completed_town = result.get("address3", "")

    def divide_address(self) -> list[str]:
        return self.address.split(" ")

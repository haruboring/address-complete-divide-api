# address-complete-divide

# About

住所を補完・分割するための API で、簡単には以下の機能を提供します。

1. 郵便番号から住所を補完する
2. 住所を分割する

入力形式は以下の通りです。

```json
{
  [
    {
      "zipcode": "105-0011",
      "address": "芝公園４丁目２−８"
    },
    {
      "zipcode": "",
      "address": "東京都千代田区千代田1番1号"
    },
    {
      "zipcode": "1000014",
      "address": "永田町１丁目７−１国会議事堂１２３号室"
    }
  ]
}
```

上記リクエストに対して、下記のようなレスポンスを持ちます

```json
{
  [
    {
      "prefecture": "東京都",
      "city": "港区",
      "town": "芝公園",
      "house_number": "4-2-8",
      "building_name": "",
      "room_number": ""
    },
    {
      "prefecture": "東京都",
      "city": "千代田区",
      "town": "千代田",
      "house_number": "1-1",
      "building_name": "",
      "room_number": ""
    },
    {
      "prefecture": "東京都",
      "city": "千代田区",
      "town": "永田町",
      "house_number": "1-7-1",
      "building_name": "国会議事堂",
      "room_number": "123号室"
    }
  ]
}
```
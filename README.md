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

# How to Complete Address(検討中)

## 方法 1. 郵便番号検索 API を叩いて住所を補完する

[郵便番号検索 API](http://zipcloud.ibsnet.co.jp/doc/api) を利用する

endpoint は次の通り https://zipcloud.ibsnet.co.jp/api/search

（例）郵便番号「7830060」で検索する場合
https://zipcloud.ibsnet.co.jp/api/search?zipcode=7830060

Response は次の通り

```json
{
	"message": null,
	"results": [
		{
			"address1": "北海道",
			"address2": "美唄市",
			"address3": "上美唄町協和",
			"kana1": "ﾎｯｶｲﾄﾞｳ",
			"kana2": "ﾋﾞﾊﾞｲｼ",
			"kana3": "ｶﾐﾋﾞﾊﾞｲﾁｮｳｷｮｳﾜ",
			"prefcode": "1",
			"zipcode": "0790177"
		},
		{
			"address1": "北海道",
			"address2": "美唄市",
			"address3": "上美唄町南",
			"kana1": "ﾎｯｶｲﾄﾞｳ",
			"kana2": "ﾋﾞﾊﾞｲｼ",
			"kana3": "ｶﾐﾋﾞﾊﾞｲﾁｮｳﾐﾅﾐ",
			"prefcode": "1",
			"zipcode": "0790177"
		}
	],
	"status": 200
}
```

### Merit

- DB を作成する必要がないので実装が容易(多分)
- 郵便番号と住所の対応に変動があってもこちらで対応する必要がない

### Demerit

- フロント -> API -> 郵便番号検索 API は少し冗長な気がする
  - ボトルネックになって方法 2 よりも実行時間がかかりそう

## 方法 2. 郵便番号データの DB を作成して住所を補完する

[郵便番号データ](http://zipcloud.ibsnet.co.jp/) を利用する

CSV 形式で
郵便番号, 都道府県, 市区町村, 町域, 都道府県カナ, 市区町村カナ, 町域カナ
という形式でデータが提供されているので、これを DB に登録して利用する。

### Merit

- DB を作成することで API を叩くよりは高速に処理ができそう

### Demerit

- DB を作成する必要があるので実装が少し面倒
- 郵便番号と住所の対応に変化があれば、迅速に DB を更新する必要がある


# How to Divide Address

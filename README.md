# address-complete-divide

![pytest](https://github.com/haruboring/address-complete-divide/actions/workflows/pytest.yml/badge.svg)
![flake8 & black](https://github.com/haruboring/address-complete-divide/actions/workflows/linter.yml/badge.svg)
[![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/haruboring/9c19de175b7ce5bcfd2eb2ed26a60d40/raw/pytest-coverage-comment.json)](https://github.com/haruboring/address-complete-divide-api/actions/workflows/pytest.yml)

## About

住所を補完・分割するための API で、簡単には以下の機能を提供します。

1. 郵便番号から住所を補完する
2. 住所を分割する

<details><summary> Request Body </summary>

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

</details>

上記リクエストに対して、下記のようなレスポンスを期待します

<details><summary> Response Body </summary>

```json
{
	"completed_count": 2,
	"addresses": [
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
			"city": "永田町",
			"town": "",
			"house_number": "1-7-1",
			"building_name": "国会議事堂",
			"room_number": "123号室"
		}
	]
}
```

</details>

## EndPoints

### POST /convert/complete_and_divide_address - 郵便番号から住所を補完し、分割する

簡単な仕様については上記の通り。
詳しい仕様については、[**How to Complete and Divide Address**](#how-to-complete-and-divide-address) を参照すること。

### GET /health - 正常にサーバーが動いているかの確認

正常であるとき、

```
{
  "status": "ok"
}
```

を返す

### /docs - FastAPI の Swagger UI

上の[2 つのエンドポイント](#endpoints)を実際に叩き、挙動を確認することができる。

## How to get address info from zipcode(検討中)

### 方法 1. 郵便番号検索 API を叩いて住所を補完する

[郵便番号検索 API](http://zipcloud.ibsnet.co.jp/doc/api) を利用する

#### [利用規約](http://zipcloud.ibsnet.co.jp/rule/api)

<details><summary> 禁止事項 </summary>

> ユーザは、本 API の利用に際して、以下の各号に定める事項を行ってはならないものとします。
>
> 1. 形態の如何を問わず、本規約の定めに反する態様で本 API を利用すること
> 2. 本 API により提供される機能のみを提供することを目的とした対象サイトにおいて本 API を利用すること、およびこれと同視し得るような態様にて対象サイトにて本 API を利用すること
> 3. 法律、規則、条例等の制定法に反する行為、又はそれを勧誘・助長する行為
> 4. 虚偽の情報をコンテンツに掲載し、コンテンツ閲覧者を欺く行為
> 5. 当社または第三者の知的財産権その他の権利を侵害する内容
> 6. 本 API の運営、又はネットワークやシステムを妨害する行為
> 7. 当社が、過度若しくは不適切と判断する商用目的の宣伝・広告行為
> 8. 有害なコンピュータウィルス、コード、ファイル、プログラム等を開示する行為、若しくは開示されている場所について示唆する行為
> 9. 犯罪行為に関わる内容、差別的表現その他公序良俗に反する内容
> 10. アダルトコンテンツ、不潔またはグロテスクなコンテンツ等一般人が不快感を覚える内容その他青少年も含めた不特定多数のユーザによる閲覧に適さない内容
> 11. 選挙の事前運動、選挙運動またはこれらに類似する行為、および公職選挙法に抵触する行為
> 12. その他公序良俗、一般常識に反する行為
> 13. その他当社が不適切であると判断する行為

</details>

endpoint は次の通り https://zipcloud.ibsnet.co.jp/api/search

（例）郵便番号「7830060」で検索する場合
https://zipcloud.ibsnet.co.jp/api/search?zipcode=7830060

<details><summary> Response は以下の通り </summary>

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

</details>

#### Merit

- DB を作成する必要がないので実装が容易(多分)
- 郵便番号と住所の対応に変動があってもこちらで対応する必要がない

#### Demerit

- フロント -> API -> 郵便番号検索 API は少し冗長な気がする
  - ボトルネックになって方法 2 よりも実行時間がかかりそう

### 方法 2. 郵便番号データの DB を作成して住所を補完する

[郵便番号データ](http://zipcloud.ibsnet.co.jp/) を利用する

CSV 形式で
郵便番号, 都道府県, 市区町村, 町域, 都道府県カナ, 市区町村カナ, 町域カナ
という形式でデータが提供されているので、これを DB に登録して利用する。

#### Merit

- DB を作成することで API を叩くよりは高速に処理ができそう

#### Demerit

- DB を作成する必要があるので実装が少し面倒
- 郵便番号と住所の対応に変化があれば、迅速に DB を更新する必要がある

## How to Complete and Divide Address

後々追記予定

## How to Use

Up the docker container
if change requirements.txt or Dockerfile or docker-compose.yml

```bash
docker-compose build
```

And

```bash
docker-compose up
```

And Access any endpoint, such as `http://0.0.0.0:8000/docs`

dependencies の更新に関しては、[Python: Create requirements.txt From Poetry](#create-requirementstxt-from-poetry)を参照。

## References

### Python

Python: 3.11.1

#### Poetry

Package Manager: Poetry [Basic Usage](https://python-poetry.org/docs/basic-usage/)

- Install a pre-existing project

  ```bash
  poetry init
  ```

- Install a package

  ```bash
  poetry add <package>
  ```

- Activate the virtual environment

  ```bash
  poetry shell
  ```

- Install the dependencies

  ```bash
  poetry install
  ```

- Run Pytest

  ```bash
  poetry run pytest
  ```

#### Create requirements.txt From Poetry

Docker 環境では`requirements.txt`を使用するため、`poetry`から`requirements.txt`を作成する必要がある。
poetry 経由で dependencies を追加した場合は、`requirements.txt`を更新する必要がある。
また、docker compose は一度 build したイメージをキャッシュするため、`requirements.txt`を更新した場合は、`docker-compose build --no-cache`を実行する必要がある。

(もしくは `docker compose up --build`を実行すること)

```bash
poetry export --output requirements.txt
```

### FastAPI

`docker/development/Dockerfile`にて、`--reload`オプションを使用しているため、開発環境では、ファイルの変更を検知し、自動的に再起動する。

## Error Solve Log

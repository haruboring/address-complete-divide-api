def format_zipcode(zipcode: str) -> str:
    CONVERT_MAP: dict[str, str] = {
        "０": "0",
        "１": "1",
        "２": "2",
        "３": "3",
        "４": "4",
        "５": "5",
        "６": "6",
        "７": "7",
        "８": "8",
        "９": "9",
        "0": "0",
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        "8": "8",
        "9": "9",
    }

    formatted_zipcode: str = ""
    for character in zipcode:
        if character in CONVERT_MAP.keys():
            formatted_zipcode += CONVERT_MAP[character]

    return formatted_zipcode

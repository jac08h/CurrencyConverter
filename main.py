from typing import Optional, Tuple
from urllib import request
from urllib.error import HTTPError
import json

ConversionData = Tuple[float, str, str]

with open("programming/python/currency_converter/freecurrencyapi_key.txt") as fp:
    key = fp.read().strip()


def parse(query: str) -> Optional[ConversionData]:
    parts = query.split()
    if len(parts) != 4:
        print("Invalid query.")
        return
    amount, old_currency, to, new_currency = parts
    if to != "to" or len(old_currency) != 3 or len(new_currency) != 3:
        print("Invalid query.")
        return
    try:
        float_amount = float(amount)
    except ValueError:
        print("Invalid amount.")
        return

    return float_amount, old_currency.upper(), new_currency.upper()


def convert(data: ConversionData) -> Optional[float]:
    amount, base, new = data
    url = f"https://freecurrencyapi.net/api/v1/rates?base_currency={base}&apikey={key}"
    req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        api_data = json.loads(request.urlopen(req).read())
    except HTTPError:
        print("Invalid base currency.")
        return

    assert len(api_data["data"])
    for date, rates in api_data["data"].items():
        try:
            conversion_rate = rates[new]
        except KeyError:
            print("Invalid new currency.")
            return

    return conversion_rate * amount


def loop() -> None:
    while True:
        data = parse(input())
        if data is None:
            continue
        converted = convert(data)
        if converted is None:
            continue
        print(f"{converted:.2f} {data[2]}")


if __name__ == '__main__':
    loop()

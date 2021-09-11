from time import strftime
from typing import Optional, Tuple
from urllib import request
from urllib.error import HTTPError
import json
from datetime import date

ConversionData = Tuple[float, str, str]

with open("freecurrencyapi_key.txt") as fp:
    key = fp.read().strip()


def parse(query: str) -> Optional[ConversionData]:
    parts = query.split()
    if len(parts) != 4:
        print("Invalid query.")
        exit(1)
    amount, old_currency, to, new_currency = parts
    if to != "to" or len(old_currency) != 3 or len(new_currency) != 3:
        print("Invalid query.")
        exit(1)
    amount, old_currency, to, new_currency = parts
    try:
        float_amount = float(amount)
    except ValueError:
        print("Invalid amount.")
        exit(1)

    return float_amount, old_currency, new_currency


def convert(data: ConversionData) -> float:
    amount, base, new = data
    url = f"https://freecurrencyapi.net/api/v1/rates?base_currency={base}&apikey={key}"
    req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        api_data = json.loads(request.urlopen(req).read())
    except HTTPError:
        print("Invalid base currency.")
        exit(1)

    assert len(api_data["data"])
    for date, rates in api_data["data"].items():
        try:
            conversion_rate = rates[new]
        except KeyError:
            print("Invalid new currency.")
            exit(1)

    return conversion_rate * amount


if __name__ == '__main__':
    data = parse("120 CZK to EUR")
    converted = convert(data)

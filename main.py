from typing import Optional, Tuple

ConversionData = Tuple[float, str, str]

with open("freecurrencyapi_key.txt") as fp:
    key = fp.read().strip()


def parse(query: str) -> Optional[ConversionData]:
    parts = query.split()
    if len(parts) != 4:
        print("Invalid query.")
        return
    assert len(parts) == 4
    amount, old_currency, to, new_currency = parts
    if to != "to":
        print("Invalid query.")
        return
    try:
        float_amount = float(amount)
    except ValueError:
        print("Invalid amount.")
        return

    return float_amount, old_currency, new_currency


if __name__ == '__main__':
    data = parse("120 CZK to EUR")

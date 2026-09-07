import json
import time
from decimal import Decimal, ROUND_HALF_UP
from urllib.error import URLError
from urllib.request import Request, urlopen
from utils.logger import logger


MONOBANK_HOST = "api.monobank.ua"
MONOBANK_CURRENCY_URL = f"https://{MONOBANK_HOST}/bank/currency"

UAH_CODE = 980
CURRENCY_CODES = {
    "USD": 840,
    "EUR": 978,
    "UAH": 980,
}
CACHE_SECONDS = 300
_rates_cache: list[dict] | None = None
_rates_cache_time = 0.0


def get_currency_rates() -> list[dict]:
    global _rates_cache, _rates_cache_time
    current_time = time.time()
    if (
        _rates_cache is not None
        and current_time - _rates_cache_time < CACHE_SECONDS
    ):
        return _rates_cache
    request = Request(
        MONOBANK_CURRENCY_URL,
        headers={"User-Agent": "FinanceTracker/1.0"}
    )
    try:
        with urlopen(request,timeout=5) as response:
            data = json.load(response)
    except (URLError,TimeoutError,json.JSONDecodeError) as error:
        logger.error(f"Monobank currency request failed: {error}")
        raise ConnectionError(
            "Could not load currency rates from Monobank"
        ) from error
    if not isinstance(data,list):
        logger.error("Invalid currency data received from Monobank")
        raise ValueError("Invalid currency data received from Monobank")
    _rates_cache = data
    _rates_cache_time = current_time
    logger.info(f"Currency rates loaded from Monobank: {len(data)} rates")
    return data


def get_currency_rate(
    currency: str,
    rates: list[dict] | None = None
) -> dict | None:
    currency = currency.strip().upper()
    if currency not in CURRENCY_CODES:
        raise ValueError(f"Unsupported currency: {currency}")
    if currency == "UAH":
        return None
    if rates is None:
        rates = get_currency_rates()
    currency_code = CURRENCY_CODES[currency]
    for rate in rates:
        if (
            rate.get("currencyCodeA") == currency_code
            and rate.get("currencyCodeB") == UAH_CODE
        ):
            return rate
    logger.error(f"Currency rate for {currency} was not found")
    raise ValueError(
        f"Currency rate for {currency} was not found"
    )


def get_reference_rate(rate: dict) -> Decimal:
    rate_cross = rate.get("rateCross")
    if rate_cross is not None and rate_cross > 0:
        return Decimal(str(rate_cross))
    rate_buy = rate.get("rateBuy")
    rate_sell = rate.get("rateSell")
    if (
        rate_buy is not None
        and rate_sell is not None
        and rate_buy > 0
        and rate_sell > 0
    ):
        return (
            Decimal(str(rate_buy))
            + Decimal(str(rate_sell))
        ) / Decimal("2")
    if rate_buy is not None and rate_buy > 0:
        return Decimal(str(rate_buy))
    if rate_sell is not None and rate_sell > 0:
        return Decimal(str(rate_sell))
    logger.error("Invalid currency rate data")
    raise ValueError("Invalid currency rate")


def convert_currency(
    amount_cents: int,
    from_currency: str,
    to_currency: str,
    rates: list[dict] | None = None
) -> int:
    from_currency = from_currency.strip().upper()
    to_currency = to_currency.strip().upper()
    if from_currency not in CURRENCY_CODES:
        raise ValueError(
            f"Unsupported source currency: {from_currency}"
        )
    if to_currency not in CURRENCY_CODES:
        raise ValueError(
            f"Unsupported target currency: {to_currency}"
        )
    if amount_cents < 0:
        raise ValueError("Amount cannot be negative")
    if from_currency == to_currency:
        return amount_cents
    if rates is None:
        rates = get_currency_rates()
    amount = Decimal(amount_cents) / Decimal("100")
    # Convert FROM original currency TO UAH
    if from_currency == "UAH":
        amount_uah = amount
    else:
        source_rate_data = get_currency_rate(
            from_currency,
            rates
        )
        source_rate = get_reference_rate(
            source_rate_data
        )
        amount_uah = amount * source_rate
    # Convert FROM UAH TO target currency
    if to_currency == "UAH":
        converted_amount = amount_uah
    else:
        target_rate_data = get_currency_rate(
            to_currency,
            rates
        )
        target_rate = get_reference_rate(
            target_rate_data
        )
        converted_amount = amount_uah / target_rate
    converted_cents = (
        converted_amount * Decimal("100")
    ).quantize(
        Decimal("1"),
        rounding=ROUND_HALF_UP
    )
    return int(converted_cents)
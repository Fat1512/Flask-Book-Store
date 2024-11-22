from babel.numbers import format_currency


def format_currency_filter(price, currency='VND'):
    # Format the value using Babel's format_currency
    return format_currency(price, currency, locale='vi_VN')
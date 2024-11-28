from babel.numbers import format_currency
import locale
from datetime import datetime

ORDER_TYPE_TEXT = ["Đặt online", "Mua trực tiếp"]
ORDER_STATUS_TEXT = ["Đang xử lý", "Chờ giao hàng", "Đang giao hàng", "Đã hoàn thành", "Đã hủy"]
PAYMENT_METHOD_TEXT = ["Thẻ", "Tiền mặt"]
SHIPPING_METHOD_TEXT = ["Giao hàng", "Tại cửa hàng"]


def format_currency_filter(price, currency='VND'):
    # Format the value using Babel's format_currency
    return format_currency(price, currency, locale='vi_VN')


def format_datetime_filter(dt):
    locale.setlocale(locale.LC_TIME, "vi_VN.UTF-8")

    weekdays_vi = ["Th 2", "Th 3", "Th 4", "Th 5", "Th 6", "Th 7", "CN"]

    # Original datetime

    # Format components
    weekday = weekdays_vi[(dt.weekday())]  # Short weekday in Vietnamese (e.g., Th 6)
    day = dt.day  # Day of the month
    month = dt.month  # Numeric month
    year = dt.year  # Year
    time = dt.strftime("%H:%M:%S")  # Time in 24-hour format

    # Combine into desired format
    formatted_date = f"{weekday}, {day}/{month}/{year} - {time}"
    return formatted_date

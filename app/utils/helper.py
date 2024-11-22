from babel.numbers import format_currency

ORDER_TYPE_TEXT = ["Đặt online", "Mua trực tiếp"]
ORDER_STATUS_TEXT = ["Đang xử lý", "Chờ giao hàng", "Đang giao hàng", "Đã hoàn thành"]
PAYMENT_METHOD_TEXT = ["Thẻ", "Tiền mặt"]
SHIPPING_METHOD_TEXT = ["Giao hàng", "Tại cửa hàng"]

def format_currency_filter(price, currency='VND'):
    # Format the value using Babel's format_currency
    return format_currency(price, currency, locale='vi_VN')
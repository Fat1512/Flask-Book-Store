from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from urllib.parse import quote
from dotenv import dotenv_values, load_dotenv
import cloudinary
from flask_login import LoginManager
from app.utils.helper import format_currency_filter, format_datetime_filter, format_date_VN

app = Flask(__name__)
load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD")

app.secret_key = "8923yhr9fuwnsejksnpok@$I_I@$)opfk"
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:%s@localhost/book_store' % quote(DB_PASSWORD)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

app.config["VNPAY_URL"] = 'https://sandbox.vnpayment.vn/paymentv2/vpcpay.html'  # Use the sandbox URL for testing
app.config["VNPAY_TMN_CODE"] = 'MEBTRFP0'
app.config["VNPAY_HASH_SECRET"] = 'ILFTJ080X209IM562X1NKYTMZ70RLVJO'
app.config["VNPAY_RETURN_URL"] = 'http://127.0.0.1:5000/cart'

cloudinary.config(
    cloud_name="duk7gxwvc",
    api_key="653944787632934",
    api_secret="GY20iNSIGW6CdrY1s1cDGwMKrqY",
    secure=True
)

app.config['SQLALCHEMY_ECHO'] = True
app.config['PAGE_SIZE'] = 12
app.config['ORDER'] = 'desc'

app.config["ORDER_PAGE_SIZE"] = 6
app.config["STATISTIC_FRE_PAGE_SIZE"] = 6
app.config["STATISTIC_REVEN_PAGE_SIZE"] = 5
app.config["BOOK_PAGE_SIZE"] = 7

db = SQLAlchemy(app=app)
login = LoginManager(app)
# Register the custom filter in Jinja2
app.jinja_env.filters['currency'] = format_currency_filter
app.jinja_env.filters['datetime'] = format_datetime_filter
app.jinja_env.filters['date'] = format_date_VN()

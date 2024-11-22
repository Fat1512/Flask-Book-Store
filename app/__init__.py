from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
import cloudinary
from flask_login import LoginManager

from app.utils.helper import format_currency_filter

app = Flask(__name__)
app.secret_key = "8923yhr9fuwnsejksnpok@$I_I@$)opfk"
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:151204@localhost/book_store'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 6

cloudinary.config(
    cloud_name="duk7gxwvc",
    api_key="653944787632934",
    api_secret="GY20iNSIGW6CdrY1s1cDGwMKrqY",
    secure=True
)

app.config['SQLALCHEMY_ECHO'] = True
app.config['PAGE_SIZE'] = 12
app.config['ORDER'] ='desc'

app.config["ORDER_PAGE_SIZE"] = 6

db = SQLAlchemy(app=app)
login = LoginManager(app)
# Register the custom filter in Jinja2
app.jinja_env.filters['currency'] = format_currency_filter

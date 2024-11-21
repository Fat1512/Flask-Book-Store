from babel.numbers import format_currency
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.utils.helper import format_currency_filter

app = Flask(__name__)
app.secret_key = "8923yhr9fuwnsejksnpok@$I_I@$)opfk"
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:090224T%40n@localhost/book_store'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config['PAGE_SIZE'] =12
app.config['ORDER'] ='desc'
db = SQLAlchemy(app=app)
# Register the custom filter in Jinja2
app.jinja_env.filters['currency'] = format_currency_filter
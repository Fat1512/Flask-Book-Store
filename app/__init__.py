from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
import cloudinary
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "8923yhr9fuwnsejksnpok@$I_I@$)opfk"
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:123456@localhost/book_store'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 6

# db = SQLAlchemy(app)

cloudinary.config(
    cloud_name="duk7gxwvc",
    api_key="653944787632934",
    api_secret="GY20iNSIGW6CdrY1s1cDGwMKrqY",
    secure=True
)

app.config['SQLALCHEMY_ECHO'] = True
app.config['PAGE_SIZE'] =12
app.config['ORDER'] ='desc'
db = SQLAlchemy(app=app)
login = LoginManager(app)

from flask import Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
import cloudinary

app = Flask(__name__)
app.secret_key = "HJGSHJS*&&*@#@&HSJAGDHJDHJFD"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/book_store?charset=utf8mb4" % quote('151204')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 6

db = SQLAlchemy(app)

cloudinary.config(
    cloud_name="duk7gxwvc",
    api_key="653944787632934",
    api_secret="GY20iNSIGW6CdrY1s1cDGwMKrqY",
    secure=True
)

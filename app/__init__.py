from flask import Flask
from flask_sqlalchemy import SQLAlchemy
<<<<<<< HEAD
from urllib.parse import quote
import cloudinary
=======
>>>>>>> 42c341449c7c759e9578e91d7b112b705a3c903d

app = Flask(__name__)
app.secret_key = "8923yhr9fuwnsejksnpok@$I_I@$)opfk"
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:151204@localhost/book_store'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
<<<<<<< HEAD
app.config["PAGE_SIZE"] = 6

db = SQLAlchemy(app)

cloudinary.config(
    cloud_name="duk7gxwvc",
    api_key="653944787632934",
    api_secret="GY20iNSIGW6CdrY1s1cDGwMKrqY",
    secure=True
)
=======
app.config['SQLALCHEMY_ECHO'] = True
app.config['PAGE_SIZE'] =12
app.config['ORDER'] ='desc'
db = SQLAlchemy(app=app)
>>>>>>> 42c341449c7c759e9578e91d7b112b705a3c903d

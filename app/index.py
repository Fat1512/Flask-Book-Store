from flask import render_template
import json
from app import app

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/category")
def get_category():
    with open('data/category.json') as f:
        data = json.load(f)
        categories = data[0:4]
    return categories

@app.route("/login")
def login_process():
    return render_template("login.html")

@app.route("/register")
def register_process():
    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)
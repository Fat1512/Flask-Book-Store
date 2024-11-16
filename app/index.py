from flask import render_template
import json
from app import app

@app.route("/")
def index():

    with open('data/category.json') as f:
        data = json.load(f)
        category_section = data[4:8]
    advertised_category_image = [
        'https://res.cloudinary.com/dq27ted4k/image/upload/v1731746970/tvy6sddbfpmg7y28ny3j.webp',
        'https://res.cloudinary.com/dq27ted4k/image/upload/v1731746969/yin3pb2nwlk7bqeqcjpx.webp',
        'https://res.cloudinary.com/dq27ted4k/image/upload/v1731746969/mtfd7avuzgrpuotg7aej.webp',
        'https://res.cloudinary.com/dq27ted4k/image/upload/v1731746969/rw19jx9s8295npm171bm.webp'
    ]

    with open('data/new_release.json') as f:
        data = json.load(f)
        new_release = data[0:8]

    bestselling_books = {}


    idx = 0
    for category in category_section:
        category['advertised_image'] = advertised_category_image[idx]
        idx += 1

    return render_template("home.html",
                           bestselling_books=bestselling_books,
                           new_release=new_release,
                           category_section=category_section)

@app.route("/category")
def get_category():
    with open('data/category.json') as f:
        data = json.load(f)
        categories = data[0:4]

    return categories

if __name__ == "__main__":
    app.run(debug=True)
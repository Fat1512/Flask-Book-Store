from flask import Blueprint
from flask import render_template, request
import json

index_bp = Blueprint('index', __name__)


@index_bp.route("/")
def index():
    with open('data/category.json', encoding="utf8") as f:
        data = json.load(f)
        category_section = data[4:8]
    advertised_category_image = [
        'https://res.cloudinary.com/dq27ted4k/image/upload/v1731746970/tvy6sddbfpmg7y28ny3j.webp',
        'https://res.cloudinary.com/dq27ted4k/image/upload/v1731746969/yin3pb2nwlk7bqeqcjpx.webp',
        'https://res.cloudinary.com/dq27ted4k/image/upload/v1731746969/mtfd7avuzgrpuotg7aej.webp',
        'https://res.cloudinary.com/dq27ted4k/image/upload/v1731746969/rw19jx9s8295npm171bm.webp'
    ]
    idx = 0
    for category in category_section:
        category['advertised_image'] = advertised_category_image[idx]
        idx += 1

    with open('data/new_release.json', encoding="utf8") as f:
        data = json.load(f)
        new_release = data[0:8]

    with open('data/bestselling_book.json', encoding="utf8") as f:
        data = json.load(f)
        bestselling_books = data[0:5]

    return render_template("home.html",
                           bestselling_books=bestselling_books,
                           new_release=new_release,
                           category_section=category_section)

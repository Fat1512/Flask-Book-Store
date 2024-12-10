from flask import Blueprint
from flask import render_template, request
import json
from app.utils.admin import profile
from datetime import datetime
from flask_login import current_user
from app.model.User import User
from flask import jsonify
from app import db


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


@index_bp.route('/update-profile', methods=['POST'])
def update_profile():
    data = request.get_json()

    try:
        user = User.query.filter_by(user_id=current_user.user_id).first()

        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404

        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.phone_number = data.get('phone_number', user.phone_number)
        user.sex = data.get('sex', user.sex)
        user.date_of_birth = data.get('date_of_birth', user.date_of_birth)
        user.avt_url = data.get('avt_url', user.avt_url)

        db.session.commit()

        return jsonify({"success": True, "updated": data}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500


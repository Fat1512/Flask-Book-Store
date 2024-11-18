from flask import request, Blueprint
from app import app
from app.dao.BookGerneDAO import get_depth_gerne

book_gerne_rest_bp = Blueprint('book_gerne_rest', __name__)


@book_gerne_rest_bp.route('/', methods=['GET'])
def get_book_gerne():
    gerne_id = request.args.get('gerneId')
    return get_depth_gerne(int(gerne_id))

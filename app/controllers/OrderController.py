import pdb

from flask import Blueprint, request, render_template
from app import app
from app.dao.OrderDAO import *
from flask import jsonify, json


order_bp = Blueprint('order', __name__)

@order_bp.route("/<order_id>")
def test(order_id):
    order = find_by_id(order_id)
    return order.to_dict()

if __name__ == "__main__":
    app.run(debug=True)

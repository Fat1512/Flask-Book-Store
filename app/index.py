import json
from threading import Thread

from elasticsearch import Elasticsearch

import app.controllers.AccountController
from app.controllers.CartController import cart_bp
from app.controllers.rest.AccountAPI import account_rest_bp
from app.controllers.rest.CartAPI import cart_rest_bp
from app.controllers.rest.PaymentAPI import payment_rest_bp
from app.dao import UserDao
from app import app, login, consumers
from app.dao.CartDao import find_by_cart_id
from app.exception.NotFoundError import NotFoundError
from app.model.User import UserRole
from flask import render_template, request, redirect, url_for, jsonify
from app.controllers.SearchController import home_bp
from app.controllers.HomeController import index_bp
from app.controllers.EmployeeController import employee_bp
from app.controllers.OrderController import order_bp
from app.controllers.rest.BookController import book_rest_bp
from app.controllers.rest.AccountAPI import account_rest_bp
from app.controllers.rest.ConfigAPI import config_api_bp
from app.controllers.rest.OrderAPI import order_api_bp
from app.controllers.rest.BookGerneController import book_gerne_rest_bp
from app.controllers.AccountController import account_bp
from app.controllers.AdminController import admin_bp
from app.controllers.CartController import cart_bp
from app.controllers.rest.CartAPI import cart_rest_bp

app.register_blueprint(home_bp, url_prefix='/search')
app.register_blueprint(employee_bp, url_prefix='/employee')
app.register_blueprint(order_bp, url_prefix='/order')

app.register_blueprint(config_api_bp, url_prefix='/api/v1/config')
app.register_blueprint(book_gerne_rest_bp, url_prefix='/api/v1/bookGerne')
app.register_blueprint(book_rest_bp, url_prefix='/api/v1/book')
app.register_blueprint(order_api_bp, url_prefix='/api/v1/order')
app.register_blueprint(cart_rest_bp, url_prefix='/api/v1/cart')
app.register_blueprint(payment_rest_bp, url_prefix='/api/v1/payment')

app.register_blueprint(account_rest_bp, url_prefix='/api/v1/account')
app.register_blueprint(index_bp, url_prefix='/')
app.register_blueprint(account_bp, url_prefix='/account')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(cart_bp, url_prefix='/cart')


@app.errorhandler(NotFoundError)
def handle_custom_error(e):
    return jsonify({
        "error": e.message,
        'status': e.status_code
    })


@app.context_processor
def cart_context():
    cart = find_by_cart_id(2)
    cart_items = cart.cart_items
    total_price = cart.total_price()

    return {
        "cart_items": cart_items,
        "total_price": total_price
    }


def consume_kafka(topic):
    """Consume messages from Kafka and index them into Elasticsearch."""
    consumer = consumers[topic]
    consumer.subscribe([topic])
    print("ok")
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        elif msg.error():
            print(msg.error())
        else:
            print('process')
            data = json.loads(msg.value().decode('utf-8'))
            handler_message(topic, data)
    consumer.close()


def handler_message(topic, data):
    if topic.__eq__("dbs_.book_store.book"):
        pass
    elif topic.__eq__("dbs_.book_store.attribute"):
        pass
    elif topic.__eq__("dbs_.book_store.book_gerne"):
        pass
    elif topic.__eq__("dbs_.book_store.extended_book"):
        pass

def handle_topic_book(data):
    pass

def handle_topic_attribute(data):
    pass

def handle_topic_book_gerne(data):
    pass

def handle_topic_extended_book(data):
    pass




# HTTP endpoint to start Kafka consumer for indexing into Elasticsearch
# @app.route('/listen/<topic>', methods=['GET'])
# def listen_topic(topic):
#     try:
#         consume_and_index(topic)
#         return jsonify({'status': 'Listening for messages'}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
#
#
# @app.route('/status', methods=['GET'])
# def status():
#     threads = [{"name": t.name, "alive": t.is_alive()} for t in threading.enumerate()]
#     return jsonify({"threads": threads})


if __name__ == "__main__":
    KAFKA_TOPICS = app.config["KAFKA_TOPIC"]
    for topic in KAFKA_TOPICS:
        consumer_thread = Thread(target=consume_kafka, args=(topic,), daemon=True)
        consumer_thread.start()

    app.run(debug=True)

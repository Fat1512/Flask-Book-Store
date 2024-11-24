import app.controllers.AccountController
from app.controllers.CartController import cart_bp
from app.dao import UserDao
from app import app, login
from app.model.User import UserRole
from flask import render_template, request, redirect, url_for
from app.controllers.SearchController import home_bp
from app.controllers.HomeController import index_bp
from app.controllers.EmployeeController import employee_bp
from app.controllers.OrderController import order_bp
from app.controllers.rest.BookController import book_rest_bp
from app.controllers.rest.OrderAPI import order_api_bp
from app.controllers.rest.BookGerneController import book_gerne_rest_bp
from app.controllers.AccountController import account_bp
from app.controllers.AdminController import admin_bp

app.register_blueprint(home_bp, url_prefix='/search')
app.register_blueprint(employee_bp, url_prefix='/employee')
app.register_blueprint(order_bp, url_prefix='/order')

app.register_blueprint(book_gerne_rest_bp, url_prefix='/api/v1/bookGerne')
app.register_blueprint(book_rest_bp, url_prefix='/api/v1/book')
app.register_blueprint(order_api_bp, url_prefix='/api/v1/order')

app.register_blueprint(index_bp, url_prefix='/')
app.register_blueprint(account_bp, url_prefix='/account')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(cart_bp,url_prefix='/cart')

if __name__ == "__main__":
    app.run(debug=True)

from flask import render_template

from app import app
from flask import render_template
from app.controllers.SearchController import home_bp
from app.controllers.HomeController import index_bp
from app.controllers.EmployeeController import employee_bp
from app.controllers.OrderController import order_bp
from app.controllers.rest.OrderAPI import order_api_bp
from app.controllers.rest.BookGerneController import book_gerne_rest_bp

app.register_blueprint(home_bp, url_prefix='/search')
app.register_blueprint(employee_bp, url_prefix='/employee')
app.register_blueprint(order_bp, url_prefix='/order')
app.register_blueprint(book_gerne_rest_bp, url_prefix='/api/v1/bookGerne')
app.register_blueprint(order_api_bp, url_prefix='/api/v1/order')
app.register_blueprint(index_bp, url_prefix='/')

@app.route("/home")
def home_process():
    return render_template("employee-order-update.html")

@app.route("/login")
def login_process():
    return render_template("login.html")

@app.route("/register")
def register_process():
    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)

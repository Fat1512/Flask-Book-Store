from flask import render_template
import dao.UserDao
from app import app, login
from flask import render_template, request, redirect
from app.controllers.SearchController import home_bp
from app.controllers.HomeController import index_bp
from app.controllers.EmployeeController import employee_bp
from app.controllers.OrderController import order_bp
from app.controllers.rest.OrderAPI import order_api_bp
from app.controllers.rest.BookGerneController import book_gerne_rest_bp
from flask_login import login_user, logout_user

app.register_blueprint(home_bp, url_prefix='/search')
app.register_blueprint(employee_bp, url_prefix='/employee')
app.register_blueprint(order_bp, url_prefix='/order')
app.register_blueprint(book_gerne_rest_bp, url_prefix='/api/v1/bookGerne')
app.register_blueprint(order_api_bp, url_prefix='/api/v1/order')
app.register_blueprint(index_bp, url_prefix='/')

@app.route("/add-products")
def add_products_process():
    return render_template("employee-order-detail.html")

@app.route("/admin-statistic")
def admin_statistic_process():
    return render_template("admin-statistic.html")

@app.route("/login", methods=['get', 'post'])
def login_process():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        u = dao.UserDao.auth_user(username=username, password=password)
        if u:
            login_user(u)
            return redirect('/employee')

    return render_template("login.html")

@app.route("/register", methods=['get', 'post'])
def register_process():
    err_msg = ''
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if password.__eq__(confirm):
            data = request.form.copy()
            del data['confirm']

            avt_url = request.files.get('avt_url')
            optional_fields = ['sex', 'phone_number', 'date_of_birth', 'isActive', 'last_access']
            for field in optional_fields:
                data[field] = data.get(field, None)
            dao.UserDao.add_user(avt_url=avt_url, **data)

            return redirect('/login')
        else:
            err_msg = 'Mật khẩu không đúng!'

    return render_template('register.html', err_msg=err_msg)

@app.route("/logout")
def logout_process():
    logout_user()
    return redirect('/employee')

@login.user_loader
def load_user(user_id):
    return dao.UserDao.get_user_by_id(user_id)

if __name__ == "__main__":
    app.run(debug=True)

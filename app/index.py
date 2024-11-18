
from app import app
from app.controllers.SearchController import home_bp
from app.controllers.employee import employee_bp

app.register_blueprint(home_bp, url_prefix='/search')
app.register_blueprint(employee_bp, url_prefix='/employee')



if __name__ == "__main__":
    app.run(debug=True)

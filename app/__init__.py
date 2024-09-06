from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_url_path='/static')
    app.config.from_pyfile('config.py')

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from app.routes.owners_routes import car_owners_bp
    from app.routes.cars_routes import cars_bp

    app.register_blueprint(car_owners_bp)
    app.register_blueprint(cars_bp)

    return app

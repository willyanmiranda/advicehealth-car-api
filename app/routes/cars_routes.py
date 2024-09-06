from flask import Blueprint, jsonify, request
from app import db
from app.models import CarOwner, Car

class CarRoutes:
    def __init__(self, blueprint):
        self.bp = blueprint
        self.register_routes()

    def register_routes(self):
        @self.bp.route('/cars', methods=['POST'])
        def add_car():
            data = request.json
            color = data.get('color')
            model = data.get('model')
            owner_id = data.get('owner_id')

            owner = self.get_owner(owner_id)
            if not owner:
                return jsonify(message='Owner does not exist'), 404

            if self.owner_has_max_cars(owner_id):
                return jsonify(message='Owner already has maximum allowed cars'), 400

            if not self.is_valid_color_and_model(color, model):
                return jsonify(message="Invalid color or model. Valid: colors ['yellow', 'blue', 'gray'], "
                                       "models: ['hatch', 'sedan', 'convertible']"), 400

            if self.owner_has_same_model(owner_id, model):
                return jsonify(message=f'Owner already has a {model} model car'), 400

            return self.create_and_add_car(color, model, owner_id)

        @self.bp.route('/cars/<int:car_id>', methods=['DELETE'])
        def delete_car(car_id):
            car = Car.query.get(car_id)
            if not car:
                return jsonify(message='Car not found'), 404

            try:
                db.session.delete(car)
                db.session.commit()
                return jsonify(message='Car deleted successfully'), 200
            except Exception as e:
                db.session.rollback()
                return jsonify(message=str(e)), 500

    def get_owner(self, owner_id):
        return CarOwner.query.get(owner_id)

    def owner_has_max_cars(self, owner_id):
        car_count = Car.query.filter_by(owner_id=owner_id).count()
        return car_count >= 3

    def is_valid_color_and_model(self, color, model):
        valid_colors = ['yellow', 'blue', 'gray']
        valid_models = ['hatch', 'sedan', 'convertible']
        return color in valid_colors and model in valid_models

    def owner_has_same_model(self, owner_id, model):
        existing_car_same_model = Car.query.filter_by(owner_id=owner_id, model=model).first()
        return existing_car_same_model is not None

    def create_and_add_car(self, color, model, owner_id):
        try:
            new_car = Car(color=color, model=model, owner_id=owner_id)
            db.session.add(new_car)
            db.session.commit()
            return jsonify(message='Car added successfully'), 201
        except Exception as e:
            db.session.rollback()
            return jsonify(message=str(e)), 400

cars_bp = Blueprint('cars', __name__)
car_routes = CarRoutes(cars_bp)

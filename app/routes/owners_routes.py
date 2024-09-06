from flask import Blueprint, jsonify, request
from app import db
from app.models import CarOwner, Car


class CarOwnerRoutes:
    def __init__(self, blueprint):
        self.bp = blueprint
        self.register_routes()

    def register_routes(self):
        @self.bp.route('/owners', methods=['POST'])
        def add_car_owner():
            data = request.json
            name = data.get('name')
            email = data.get('email')

            try:
                new_owner = CarOwner(name=name, email=email)
                db.session.add(new_owner)
                db.session.commit()
                return jsonify(message='Car owner added successfully', owner_id=new_owner.id), 201
            except Exception as e:
                db.session.rollback()
                return jsonify(message=str(e)), 500

        @self.bp.route('/owners', methods=['GET'])
        def get_car_owners():
            try:
                owners = CarOwner.query.all()
                owners_list = [{"id": owner.id, "name": owner.name, "email": owner.email} for owner in owners]
                return jsonify(owners_list), 200
            except Exception as e:
                return jsonify(message=str(e)), 500

        @self.bp.route('/owners/<int:owner_id>/cars', methods=['GET'])
        def get_cars_by_owner(owner_id):
            try:
                cars = Car.query.filter_by(owner_id=owner_id).all()
                cars_list = [{"id": car.id, "color": car.color, "model": car.model, "owner_id": car.owner_id} for car in
                             cars]
                return jsonify(cars_list), 200
            except Exception as e:
                return jsonify(message=str(e)), 400

        @self.bp.route('/owners/<int:owner_id>', methods=['DELETE'])
        def delete_car_owner(owner_id):
            try:
                owner = CarOwner.query.get(owner_id)
                if owner is None:
                    return jsonify(message="Owner not found"), 404

                Car.query.filter_by(owner_id=owner_id).delete()
                db.session.delete(owner)
                db.session.commit()
                return jsonify(message="Car owner and associated cars deleted successfully"), 200
            except Exception as e:
                db.session.rollback()
                return jsonify(message=str(e)), 500

        @self.bp.route('/')
        def base_connection():
            return "Hello, World!"


car_owners_bp = Blueprint('car_owners', __name__)
car_owner_routes = CarOwnerRoutes(car_owners_bp)

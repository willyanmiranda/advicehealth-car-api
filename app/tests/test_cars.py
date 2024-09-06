import unittest
import json
from flask import Flask

from app import db
from app.models import CarOwner, Car
from app.routes.cars_routes import car_routes


class CarRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.register_blueprint(car_routes.bp)

        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        self.client = self.app.test_client()

        self.db = db
        self.db.init_app(self.app)
        with self.app.app_context():
            self.db.create_all()

    def tearDown(self):
        """Clean up after tests."""
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()

    def test_add_car(self):
        with self.app.app_context():
            owner = CarOwner(name='Test Owner', email='test@example.com')
            self.db.session.add(owner)
            self.db.session.commit()

            data = {
                'color': 'yellow',
                'model': 'hatch',
                'owner_id': owner.id
            }
            response = self.client.post('/cars', json=data)
            self.assertEqual(response.status_code, 201)

            json_data = json.loads(response.data)
            self.assertEqual(json_data['message'], 'Car added successfully')

    def test_delete_car(self):
        with self.app.app_context():
            car = Car(color='blue', model='sedan', owner_id=1)
            self.db.session.add(car)
            self.db.session.commit()

            response = self.client.delete(f'/cars/{car.id}')
            self.assertEqual(response.status_code, 200)

            json_data = json.loads(response.data)
            self.assertEqual(json_data['message'], 'Car deleted successfully')

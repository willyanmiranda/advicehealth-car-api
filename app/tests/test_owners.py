import unittest
import json
from flask import Flask

from app import db
from app.models import CarOwner, Car
from app.routes.owners_routes import car_owner_routes


class CarOwnerRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.register_blueprint(car_owner_routes.bp)

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

    def test_add_car_owner(self):
        with self.app.app_context():
            data = {
                'name': 'Falamansa',
                'email': 'falamsansa@example.com'
            }
            response = self.client.post('/owners', json=data)
            self.assertEqual(response.status_code, 201)

            json_data = json.loads(response.data)
            self.assertEqual(json_data['message'], 'Car owner added successfully')
            self.assertIn('owner_id', json_data)

    def test_get_car_owners(self):
        with self.app.app_context():
            owner1 = CarOwner(name='Junin', email='junin@example.com')
            owner2 = CarOwner(name='Osnildo', email='osnildo@example.com')
            self.db.session.add_all([owner1, owner2])
            self.db.session.commit()

            response = self.client.get('/owners')
            self.assertEqual(response.status_code, 200)

            json_data = json.loads(response.data)
            self.assertIsInstance(json_data, list)
            self.assertEqual(len(json_data), 2)

            self.assertEqual(json_data[0]['name'], 'Junin')
            self.assertEqual(json_data[1]['name'], 'Osnildo')

    def test_get_cars_by_owner(self):
        with self.app.app_context():
            owner = CarOwner(name='Messi', email='messi@example.com')
            self.db.session.add(owner)
            self.db.session.commit()

            car1 = Car(color='blue', model='sedan', owner_id=owner.id)
            car2 = Car(color='red', model='hatch', owner_id=owner.id)
            self.db.session.add_all([car1, car2])
            self.db.session.commit()

            response = self.client.get(f'/owners/{owner.id}/cars')
            self.assertEqual(response.status_code, 200)

            json_data = json.loads(response.data)
            self.assertIsInstance(json_data, list)
            self.assertEqual(len(json_data), 2)

            self.assertEqual(json_data[0]['color'], 'blue')
            self.assertEqual(json_data[1]['color'], 'red')

    def test_delete_car_owner(self):
        with self.app.app_context():
            owner = CarOwner(name='Eve', email='eve@example.com')
            self.db.session.add(owner)
            self.db.session.commit()

            response = self.client.delete(f'/owners/{owner.id}')
            self.assertEqual(response.status_code, 200)

            json_data = json.loads(response.data)
            self.assertEqual(json_data['message'], 'Car owner and associated cars deleted successfully')

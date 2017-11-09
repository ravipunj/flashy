import unittest

from app import api_manager, app, db

app.config.from_object('config.TestingConfig')

db.app = app
db.init_app(app)

api_manager.app = app
api_manager.init_app(app)

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        db.create_all()

        self.test_client = app.test_client()
        self.db = db

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

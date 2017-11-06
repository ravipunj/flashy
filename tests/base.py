import unittest

from app import app, db

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config.TestingConfig')
        db.create_all()

        self.app = app
        self.db = db

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

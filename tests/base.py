import unittest

from app import app, db

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config.TestingConfig')
        db.session = db.create_scoped_session()
        db.create_all()

        self.test_client = app.test_client()
        self.db = db

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

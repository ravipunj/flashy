import os
import unittest

from app import app, db

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        assert os.environ["APP_SETTINGS"] == "config.TestingConfig"
        db.create_all()

        self.test_client = app.test_client()
        self.db = db

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

from flask_testing import TestCase

from app import app, db


class BaseTestCase(TestCase):
    maxDiff = None

    def create_app(self):
        app.config.from_object("config.TestingConfig")
        return app

    def setUp(self):
        db.create_all()

        self.test_client = app.test_client()
        self.db = db

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

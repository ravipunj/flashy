from tests.base import BaseTestCase

from sqlalchemy.exc import DataError, IntegrityError

from models.user import User


def create_user(db_session, **overrides):
    params = dict(
        username="cooldude100",
        password_hash="938hqt98h3t89u92",
        password_salt="ottffssentettffs",
        display_name="Ravi Punj",
        email="ravi@ravipunj.com",
    )
    params.update(overrides)

    user = User(**params)

    db_session.add(user)
    db_session.commit()

    return user

class UserModelTest(BaseTestCase):
    def create_user(self, **overrides):
        return create_user(self.db.session, **overrides)

    def assert_raises_integrity_error_for_null_field(self, field_name):
        self.assertRaises(IntegrityError, self.create_user, **{field_name: None})

    def test_raises_integrity_error_if_username_is_null(self):
        self.assert_raises_integrity_error_for_null_field("username")

    def test_raises_integrity_error_if_password_hash_is_null(self):
        self.assert_raises_integrity_error_for_null_field("password_hash")

    def test_raises_integrity_error_if_password_salt_is_null(self):
        self.assert_raises_integrity_error_for_null_field("password_salt")

    def test_raises_integrity_error_if_display_name_is_null(self):
        self.assert_raises_integrity_error_for_null_field("display_name")

    def test_raises_integrity_error_if_email_is_null(self):
        self.assert_raises_integrity_error_for_null_field("email")

    def test_raises_data_error_if_salt_is_longer_than_sixteen_characters(self):
        self.assertRaises(DataError, self.create_user, password_salt="ottffssentettffss")

    def test_constructs_user(self):
        user1 = self.create_user()

        self.assertEqual(User.query.one(), user1)

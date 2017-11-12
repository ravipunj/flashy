import json

import mock

from tests.base import BaseTestCase
from models import mixins


API_URL = "/api/user"
HEADERS = [("Content-Type", "application/json"),
           ("Accept", "application/json")]
USERNAME = "TESTUSER"
PASSWORD = "strongestpasswordeva"
DISPLAY_NAME = "Test User"
EMAIL = "unit@test.com"


def _get_sample_new_user_data():
    return {
        "username": USERNAME,
        "password": PASSWORD,
        "display_name": DISPLAY_NAME,
        "email": EMAIL,
    }


def _get_sample_existing_user_data(**overrides):
    user_data = {
        "username": USERNAME,
        "display_name": DISPLAY_NAME,
        "email": EMAIL,
        "decks": [],
    }
    user_data.update(overrides)

    return user_data


class TestUserBase(BaseTestCase):
    def post_user(self, data):
        return self.test_client.post(API_URL, headers=HEADERS, data=json.dumps(data))

    def get_user(self, user_id):
        return self.test_client.get("%s/%s" % (API_URL, user_id), headers=HEADERS)


class TestPostUser(TestUserBase):
    @mock.patch.object(mixins, "generate_uuid4_string", return_value="stub_id")
    def test_creates_new_user(self, _):
        user_data = _get_sample_new_user_data()

        response = self.post_user(data=user_data)

        self.assertEqual(201, response.status_code)
        self.assertEqual("application/json", response.headers["Content-Type"])

        expected_data = _get_sample_existing_user_data(id="stub_id")
        self.assertEqual(expected_data, json.loads(response.data))


class TestGetUser(TestUserBase):

    def _add_sample_user(self):
        user_data = _get_sample_new_user_data()

        response = self.post_user(user_data)

        return json.loads(response.data)["id"]

    def test_gets_user(self):
        user_id = self._add_sample_user()

        response = self.get_user(user_id)

        self.assertEqual(200, response.status_code)
        self.assertEqual(_get_sample_existing_user_data(id=user_id), json.loads(response.data))

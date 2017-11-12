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


def _get_sample_new_user_data(**overrides):
    user_data = {
        "username": USERNAME,
        "password": PASSWORD,
        "display_name": DISPLAY_NAME,
        "email": EMAIL,
    }
    user_data.update(overrides)

    return user_data


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

    def get_all_users(self):
        return self.test_client.get(API_URL, headers=HEADERS)


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

    def _add_sample_user(self, **overrides):
        user_data = _get_sample_new_user_data(**overrides)

        response = self.post_user(user_data)

        return json.loads(response.data)["id"]

    def test_gets_user(self):
        user_id = self._add_sample_user()

        response = self.get_user(user_id)

        self.assertEqual(200, response.status_code)
        self.assertEqual(_get_sample_existing_user_data(id=user_id), json.loads(response.data))

    def test_get_all_users_returns_all_users(self):
        user1 = _get_sample_new_user_data()
        user2 = _get_sample_new_user_data(username="tu2",
                                          display_name="Test User #2",
                                          email="tu2@gmail.com")
        user1["id"] = self._add_sample_user(**user1)
        user2["id"] = self._add_sample_user(**user2)

        response = self.get_all_users()
        response_data = json.loads(response.data)
        response_data["objects"].sort(key=lambda o: o["id"])

        user1.pop("password"), user2.pop("password")
        expected_user1 = _get_sample_existing_user_data(**user1)
        expected_user2 = _get_sample_existing_user_data(**user2)
        self.assert200(response)
        self.assertDictEqual(
            {
                "total_pages": 1,
                "num_results": 2,
                "page": 1,
                "objects": sorted([expected_user1, expected_user2], key=lambda u: u["id"]),
            },
            response_data
        )

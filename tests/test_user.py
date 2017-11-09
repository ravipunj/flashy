import json

import mock

from tests.base import BaseTestCase
from models import mixins


class TestPostUser(BaseTestCase):
    def post_user(self, data):
        url = "/api/user"
        headers = [("Content-Type", "application/json"),
                   ("Accept", "application/json")]

        return self.test_client.post(url, headers=headers, data=json.dumps(data))

    @mock.patch.object(mixins, "generate_uuid4_string", return_value="stub_id")
    def test_creates_new_user(self, _):
        user_data = {
            "username": "test_user",
            "password": "strongestpasswordever",
            "display_name": "Test User",
            "email": "unit@test.com",
        }

        response = self.post_user(data=user_data)

        self.assertEqual(201, response.status_code)
        self.assertEqual("application/json", response.headers["Content-Type"])

        expected_data = {
            "id": "stub_id",
            "username": user_data["username"],
            "display_name": user_data["display_name"],
            "email": user_data["email"],
            "decks": [],
        }
        self.assertEqual(expected_data, json.loads(response.data))

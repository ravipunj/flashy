from tests.base import BaseTestCase


class TestHealth(BaseTestCase):
    def test_returns_200_OK(self):
        response = self.test_client.get("/health")

        self.assertEqual("", response.data)
        self.assertEqual("200 OK", response.status)

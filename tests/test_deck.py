import copy
import json

import mock

from tests.base import BaseTestCase

from models import mixins
from tests.test_user import get_sample_new_user_data, get_user, post_user


API_URL = "/api/deck"
HEADERS = [("Content-Type", "application/json"),
           ("Accept", "application/json")]
NAME = "French Vocab"
OWNER_DATA = get_sample_new_user_data()


def get_sample_deck_data(**overrides):
    deck_data = {
        "name": NAME,
        "cards": [],
    }
    deck_data.update(overrides)

    return deck_data


def post_deck(client, data):
    return client.post(API_URL, headers=HEADERS, data=json.dumps(data))


def get_deck(client, deck_id):
    return client.get("%s/%s" % (API_URL, deck_id), headers=HEADERS)


class TestDeckBase(BaseTestCase):
    def _get_owner(self, **overrides):
        owner_data = copy.deepcopy(OWNER_DATA)
        owner_data.update(overrides)

        owner = json.loads(post_user(self.test_client, owner_data).data)
        del owner["decks"]

        return owner

    def _add_sample_deck(self, **overrides):
        deck_data = get_sample_deck_data(**overrides)

        response = self.post_deck(deck_data)

        return json.loads(response.data)["id"]

    def post_deck(self, data):
        return post_deck(self.test_client, data)

    def get_deck(self, deck_id):
        return get_deck(self.test_client, deck_id)

    def get_all_decks(self):
        return self.test_client.get(API_URL, headers=HEADERS)

    def get_user(self, user_id):
        return json.loads(get_user(self.test_client, user_id).data)


class TestPostDeck(TestDeckBase):
    @mock.patch.object(mixins, "generate_uuid4_string", return_value="stub_id")
    def test_creates_new_deck_for_owner(self, _):
        owner = self._get_owner()
        deck_data = get_sample_deck_data(owner_id=owner["id"])

        response = self.post_deck(deck_data)

        self.assertStatus(response, 201)
        self.assertDictEqual(
            get_sample_deck_data(id="stub_id", owner=owner),
            json.loads(response.data)
        )


class TestGetDeck(TestDeckBase):

    def test_gets_deck(self):
        owner = self._get_owner()
        deck_id = self._add_sample_deck(owner_id=owner["id"])

        response = self.get_deck(deck_id)

        self.assert200(response)
        self.assertEqual(
            get_sample_deck_data(id=deck_id, owner=owner),
            json.loads(response.data)
        )

    def test_gets_all_decks(self):
        owner1 = self._get_owner(username="u1", display_name="Clyde", email="cl@y.de")
        owner2 = self._get_owner(username="u2", display_name="Bono", email="bo@no.com")
        deck1 = get_sample_deck_data(owner_id=owner1["id"])
        deck1["id"] = self._add_sample_deck(**deck1)
        deck2 = get_sample_deck_data(name="GRE Words", owner_id=owner2["id"])
        deck2["id"] = self._add_sample_deck(**deck2)

        response = self.get_all_decks()
        response_data = json.loads(response.data)
        response_data["objects"].sort(key=lambda o: o["id"])

        expected_deck1 = get_sample_deck_data(owner=owner1, **deck1)
        del expected_deck1["owner_id"]
        expected_deck2 = get_sample_deck_data(owner=owner2, **deck2)
        del expected_deck2["owner_id"]
        self.assert200(response)
        self.assertDictEqual(
            {
                "total_pages": 1,
                "num_results": 2,
                "page": 1,
                "objects": sorted([expected_deck1, expected_deck2], key=lambda d: d["id"]),
            },
            response_data
        )


class TestGetDecksForOwner(TestDeckBase):
    def test_gets_decks_for_owner(self):
        owner = self._get_owner()
        deck1 = get_sample_deck_data(name="Deck1", owner_id=owner["id"])
        deck1["id"] = self._add_sample_deck(**deck1)
        del deck1["cards"]
        deck2 = get_sample_deck_data(name="Deck2", owner_id=owner["id"])
        deck2["id"] = self._add_sample_deck(**deck2)
        del deck2["cards"]

        user = self.get_user(user_id=owner["id"])

        self.assertListEqual(
            sorted([deck1, deck2], key=lambda d: d["id"]),
            sorted(user["decks"], key=lambda d: d["id"])
        )


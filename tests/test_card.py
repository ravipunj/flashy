import copy
import json

import mock

from tests.base import BaseTestCase

from models import mixins
from tests.test_deck import get_sample_deck_data, get_deck, post_deck
from tests.test_user import get_sample_new_user_data, post_user

API_URL = "/api/card"
HEADERS = [("Content-Type", "application/json"),
           ("Accept", "application/json")]
OWNER_DATA = get_sample_new_user_data()
DECK_DATA = get_sample_deck_data()


def get_sample_card_data(**overrides):
    card_data = {
        "data": {"valid": "json"},
    }
    card_data.update(overrides)

    return card_data


def post_card(client, data):
    return client.post(API_URL, headers=HEADERS, data=json.dumps(data))


def get_card(client, card_id):
    return client.get("%s/%s" % (API_URL, card_id), headers=HEADERS)


class TestCardBase(BaseTestCase):
    def _get_owner(self, **overrides):
        owner_data = copy.deepcopy(OWNER_DATA)
        owner_data.update(overrides)

        owner = json.loads(post_user(self.test_client, owner_data).data)
        del owner["decks"]

        return owner

    def _get_deck(self, **overrides):
        deck_data = copy.deepcopy(DECK_DATA)
        deck_data.update(overrides)

        deck = json.loads(post_deck(self.test_client, deck_data).data)
        del deck["cards"]
        del deck["owner"]

        return deck

    def _add_sample_card(self, **overrides):
        card_data = get_sample_card_data(**overrides)

        response = self.post_card(card_data)

        return json.loads(response.data)["id"]

    def post_card(self, data):
        return post_card(self.test_client, data)

    def get_card(self, card_id):
        return get_card(self.test_client, card_id)

    def get_all_cards(self):
        return self.test_client.get(API_URL, headers=HEADERS)

    def get_deck(self, deck_id):
        return json.loads(get_deck(self.test_client, deck_id).data)


class TestPostCard(TestCardBase):
    @mock.patch.object(mixins, "generate_uuid4_string", return_value="stub_id")
    def test_creates_new_card_for_deck(self, _):
        owner = self._get_owner()
        deck = self._get_deck(owner_id=owner["id"])
        card_data = get_sample_card_data(deck_id=deck["id"])

        response = self.post_card(card_data)

        self.assertStatus(response, 201)
        self.assertDictEqual(
            get_sample_card_data(id="stub_id", deck=deck),
            json.loads(response.data)
        )


class TestGetCard(TestCardBase):
    def test_gets_card(self):
        owner = self._get_owner()
        deck = self._get_deck(owner_id=owner["id"])
        card_id = self._add_sample_card(deck_id=deck["id"])

        response = self.get_card(card_id)

        self.assert200(response)
        self.assertDictEqual(
            get_sample_card_data(id=card_id, deck=deck),
            json.loads(response.data)
        )

    def test_gets_all_cards(self):
        owner1 = self._get_owner(username="u1", display_name="Bob", email="bob@flashyyy.com")
        owner2 = self._get_owner(username="u2", display_name="John", email="john@flashyyy.com")
        deck1 = self._get_deck(owner_id=owner1["id"])
        card1 = get_sample_card_data(deck_id=deck1["id"])
        card1["id"] = self._add_sample_card(**card1)
        deck2 = self._get_deck(owner_id=owner2["id"])
        card2 = get_sample_card_data(deck_id=deck2["id"])
        card2["id"] = self._add_sample_card(**card2)
        card3 = get_sample_card_data(deck_id=deck2["id"])
        card3["id"] = self._add_sample_card(**card3)

        response = self.get_all_cards()
        response_data = json.loads(response.data)
        response_data["objects"].sort(key=lambda o: o["id"])

        expected_card1 = get_sample_card_data(deck=deck1, **card1)
        del expected_card1["deck_id"]
        expected_card2 = get_sample_card_data(deck=deck2, **card2)
        del expected_card2["deck_id"]
        expected_card3 = get_sample_card_data(deck=deck2, **card3)
        del expected_card3["deck_id"]
        self.assert200(response)
        self.assertDictEqual(
            {
                "total_pages": 1,
                "num_results": 3,
                "page": 1,
                "objects": sorted([expected_card1, expected_card2, expected_card3],
                                  key=lambda c: c["id"]),
            },
            response_data
        )


class TestGetCardsForDeck(TestCardBase):
    def test_gets_cards_for_deck(self):
        owner = self._get_owner()
        deck = self._get_deck(owner_id=owner["id"])
        card1 = get_sample_card_data(deck_id=deck["id"])
        card1["id"] = self._add_sample_card(**card1)
        del card1["deck_id"]
        card2 = get_sample_card_data(deck_id=deck["id"])
        card2["id"] = self._add_sample_card(**card2)
        del card2["deck_id"]
        card3 = get_sample_card_data(deck_id=deck["id"])
        card3["id"] = self._add_sample_card(**card3)
        del card3["deck_id"]

        deck = self.get_deck(deck_id=deck["id"])

        self.assertListEqual(
            sorted([card1, card2, card3], key=lambda c: c["id"]),
            sorted(deck["cards"], key=lambda c: c["id"])
        )


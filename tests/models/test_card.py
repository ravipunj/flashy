from tests.base import BaseTestCase
from tests.models.test_deck import create_deck
from tests.models.test_user import create_user

from sqlalchemy.exc import IntegrityError, StatementError

from app import db
from models.card import Card
from models.deck import Deck


def create_card(deck, **overrides):
    params = {
        "data": {"random": "data"},
        "deck": deck,
    }
    params.update(overrides)

    card = Card(**params)

    db.session.add(card)
    db.session.commit()

    return card


class TestCardModel(BaseTestCase):
    def setUp(self):
        super(TestCardModel, self).setUp()

        self.test_deck = create_deck(owner=create_user())

    def test_raises_integrity_error_if_no_data_is_set(self):
        self.assertRaises(IntegrityError, create_card, deck=self.test_deck, data=None)

    def test_raises_integrity_error_if_deck_is_invalid(self):
        self.assertRaises(IntegrityError, create_card, deck=Deck())

    def test_raises_data_error_if_data_is_not_json_serializable(self):
        self.assertRaises(StatementError, create_card, deck=self.test_deck, data=object())

    def test_creates_card(self):
        card = create_card(deck=self.test_deck)

        card_in_db = Card.query.one()

        self.assertEqual(card, card_in_db)
        self.assertEqual(self.test_deck, card_in_db.deck)
        self.assertEqual([card_in_db], self.test_deck.cards)

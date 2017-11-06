from tests.base import BaseTestCase

from sqlalchemy.exc import IntegrityError, StatementError

from models.card import Card
from models.deck import Deck
from tests.models.test_deck import create_deck


def create_card(db_session, **overrides):
    params = {
        "data": {"random": "data"},
        "deck": create_deck(db_session)
    }
    params.update(overrides)

    card = Card(**params)

    db_session.add(card)
    db_session.commit()

    return card


class TestCardModel(BaseTestCase):
    def setUp(self):
        super(TestCardModel, self).setUp()

        self.test_deck = create_deck(self.db.session)

    def create_card(self, **overrides):
        if "deck" not in overrides:
            overrides["deck"] = self.test_deck
        return create_card(self.db.session, **overrides)

    def test_raises_integrity_error_if_no_data_is_set(self):
        self.assertRaises(IntegrityError, self.create_card, data=None)

    def test_raises_integrity_error_if_deck_is_invalid(self):
        self.assertRaises(IntegrityError, self.create_card, deck=Deck())

    def test_raises_data_error_if_data_is_not_json_serializable(self):
        self.assertRaises(StatementError, self.create_card, data=object())

    def test_creates_card(self):
        card = self.create_card()

        card_in_db = Card.query.one()

        self.assertEqual(card, card_in_db)
        self.assertEqual(self.test_deck, card_in_db.deck)
        self.assertEqual([card_in_db], self.test_deck.cards)

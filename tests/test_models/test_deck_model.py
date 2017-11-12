from sqlalchemy.exc import IntegrityError

from tests.base import BaseTestCase
from tests.test_models.test_user_model import create_user

from app import db
from models.deck import Deck
from models.user import User


def create_deck(owner, **overrides):
    params = {
        "name": "My Awesome Deck",
        "owner": owner,
    }
    params.update(overrides)

    deck = Deck(**params)

    db.session.add(deck)
    db.session.commit()

    return deck


class TestDeckModel(BaseTestCase):
    def setUp(self):
        super(TestDeckModel, self).setUp()

        self.test_user = create_user()

    def test_raises_integrity_error_if_name_is_null(self):
        self.assertRaises(IntegrityError, create_deck, owner=self.test_user, name=None)

    def test_raises_error_if_owner_is_invalid(self):
        self.assertRaises(IntegrityError, create_deck, owner=User())

    def test_creates_deck(self):
        deck = create_deck(owner=self.test_user)

        deck_in_db = Deck.query.one()

        self.assertEqual(deck, deck_in_db)
        self.assertEqual(self.test_user, deck_in_db.owner)
        self.assertEqual([deck], self.test_user.decks)

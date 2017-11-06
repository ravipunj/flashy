from sqlalchemy.exc import IntegrityError

from tests.base import BaseTestCase
from tests.models.test_user import create_user

from models.deck import Deck
from models.user import User


def create_deck(db_session, **overrides):
    params = {
        "name": "My Awesome Deck",
        "owner": create_user(db_session),
    }
    params.update(overrides)

    deck = Deck(**params)

    db_session.add(deck)
    db_session.commit()

    return deck

class TestDeckModel(BaseTestCase):
    def setUp(self):
        super(TestDeckModel, self).setUp()

        self.test_user = create_user(self.db.session)

    def create_deck(self, **overrides):
        if "owner" not in overrides:
            overrides["owner"] = self.test_user

        return create_deck(self.db.session, **overrides)

    def test_raises_integrity_error_if_name_is_null(self):
        self.assertRaises(IntegrityError, self.create_deck, name=None)

    def test_raises_error_if_owner_is_invalid(self):
        self.assertRaises(IntegrityError, self.create_deck, owner=User())

    def test_creates_deck(self):
        deck = self.create_deck()

        deck_in_db = Deck.query.one()

        self.assertEqual(deck, deck_in_db)
        self.assertEqual(self.test_user, deck_in_db.owner)
        self.assertEqual([deck], self.test_user.decks)

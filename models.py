import os

import datetime
import uuid

from app import db
from sqlalchemy.dialects.postgresql import JSON
from attrs_sqlalchemy import attrs_sqlalchemy


class UUIDMixin(object):
    id = db.Column(db.String(32), primary_key=True, default=lambda: uuid.uuid4().hex)


class CreatedMixin(object):
    created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)


class ModifiedMixin(object):
    modified = db.Column(db.DateTime, nullable=False,
                         default=datetime.datetime.now, onupdate=datetime.datetime.now)


class BaseModelMixin(UUIDMixin, CreatedMixin, ModifiedMixin):
    pass


@attrs_sqlalchemy
class User(BaseModelMixin, db.Model):
    __tablename__ = "user"

    username = db.Column(db.String(), nullable=False, index=True)
    password_hash = db.Column(db.String(), nullable=False)
    password_salt = db.Column(db.String(16), nullable=False)
    display_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)


@attrs_sqlalchemy
class Deck(BaseModelMixin, db.Model):
    __tablename__ = "deck"

    name = db.Column(db.String(), nullable=False)
    owner_id = db.Column(db.String(32), db.ForeignKey("user.id"))

    owner = db.relationship("User", back_populates="decks")


User.decks = db.relationship("Deck", order_by=Deck.id, back_populates="owner")


@attrs_sqlalchemy
class Card(BaseModelMixin, db.Model):
    __tablename__ = "card"

    data = db.Column(JSON, nullable=False)
    deck_id = db.Column(db.String(32), db.ForeignKey("deck.id"))
    deck = db.relationship("Deck", back_populates="cards")


Deck.cards = db.relationship("Card", order_by=Card.id, back_populates="deck")

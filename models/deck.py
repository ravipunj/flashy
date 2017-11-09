from attrs_sqlalchemy import attrs_sqlalchemy

from app import db
from models.mixins import BaseModelMixin


@attrs_sqlalchemy
class Deck(BaseModelMixin, db.Model):
    __tablename__ = "deck"

    name = db.Column(db.String(), nullable=False)

    owner_id = db.Column(db.String(32), db.ForeignKey("user.id"))

    cards = db.relationship("Card", backref="deck")
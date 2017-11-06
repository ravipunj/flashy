from attrs_sqlalchemy import attrs_sqlalchemy

from app import db
from models.mixins import BaseModelMixin


@attrs_sqlalchemy
class User(BaseModelMixin, db.Model):
    __tablename__ = "user"

    username = db.Column(db.String(), nullable=False, index=True)
    password_hash = db.Column(db.String(), nullable=False)
    password_salt = db.Column(db.String(16), nullable=False)
    display_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)

    decks = db.relationship("Deck", backref="owner")

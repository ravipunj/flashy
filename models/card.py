from attrs_sqlalchemy import attrs_sqlalchemy
from sqlalchemy.dialects.postgresql import JSON

from app import db
from models.mixins import BaseModelMixin


@attrs_sqlalchemy
class Card(BaseModelMixin, db.Model):
    __tablename__ = "card"

    data = db.Column(JSON(none_as_null=True), nullable=False)
    deck_id = db.Column(db.String(32), db.ForeignKey("deck.id"))
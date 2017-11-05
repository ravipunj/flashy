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
class Card(BaseModelMixin, db.Model):
    __tablename__ = "card"

    data = db.Column(JSON, nullable=False)

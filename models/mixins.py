import datetime
import uuid

from app import db


class UUIDMixin(object):
    id = db.Column(db.String(32), primary_key=True, default=lambda: uuid.uuid4().hex)


class CreatedMixin(object):
    created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)


class ModifiedMixin(object):
    modified = db.Column(db.DateTime, nullable=False,
                         default=datetime.datetime.now, onupdate=datetime.datetime.now)


class BaseModelMixin(UUIDMixin, CreatedMixin, ModifiedMixin):
    pass
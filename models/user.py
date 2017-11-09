import binascii
import hashlib
import os

from attrs_sqlalchemy import attrs_sqlalchemy

from app import api_manager, db
from models.mixins import BaseModelMixin


@attrs_sqlalchemy
class User(BaseModelMixin, db.Model):
    __tablename__ = "user"

    username = db.Column(db.String(), nullable=False, unique=True)
    password_hash = db.Column(db.String(64), nullable=False)
    password_salt = db.Column(db.String(32), nullable=False)
    display_name = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)

    decks = db.relationship("Deck", backref="owner")


def process_password(data):
    password = data.pop("password")
    password_salt = binascii.hexlify(os.urandom(16))
    password_hash = binascii.hexlify(hashlib.pbkdf2_hmac("sha256",
                                                         password=password,
                                                         salt=password_salt,
                                                         iterations=40000,
                                                         dklen=32))

    data["password_salt"] = password_salt
    data["password_hash"] = password_hash

api_manager.create_api(
    User,
    methods=["POST"],
    exclude_columns=["created", "modified", "password_salt", "password_hash"],
    preprocessors={
        "POST": [process_password],
    },
)

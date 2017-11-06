import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ["APP_SETTINGS"])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

from models import *


@app.route("/health")
def health():
    return ""


if __name__ == "__main__":
    print "Config: {config}".format(config=os.environ["APP_SETTINGS"])
    app.run()

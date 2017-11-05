import os

from flask import Flask

app = Flask(__name__)
app.config.from_object(os.environ["APP_SETTINGS"])


@app.route("/health")
def health():
    return ""


if __name__ == "__main__":
    print "Config: {config}".format(config=os.environ["APP_SETTINGS"])
    app.run()

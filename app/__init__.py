from os import environ

from flask import Flask

from app.api import api


def create_flask_app():
    """Flask app factory method"""
    app = Flask(__name__)
    app.config.from_mapping(
        BCRYPT_LOG_ROUNDS=10, SECRET_KEY=environ["FLASK_SECRET_KEY"]
    )

    @app.route("/")
    def hello_world():
        return "Hello World!"

    api.init_app(app)
    return app

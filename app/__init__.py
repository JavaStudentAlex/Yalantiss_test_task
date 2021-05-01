"""Module for initialising  flask application"""
from datetime import date
from os import environ

from flask import Flask
from flask_migrate import Migrate

from app.api import api
from app.models import Course, bcrypt, db
from app.swagger import SWAGGER_UI_BLUEPRINT, SWAGGER_URL


def __add_default_course(app: Flask):
    app.app_context().push()
    db.create_all()
    if Course.query.count() == 0:
        course = Course("course", date.today(), date.today(), 1)
        db.session.add(course)
        db.session.commit()


def create_flask_app():
    """Flask app factory method"""
    app = Flask(__name__)
    app.config.from_mapping(
        BCRYPT_LOG_ROUNDS=10,
        SECRET_KEY=environ["FLASK_SECRET_KEY"],
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_DATABASE_URI=environ["DATABASE_PATH"],
    )

    @app.route("/")
    def hello_world():
        return "Hello World!"

    # init database
    db.init_app(app)
    bcrypt.init_app(app)
    Migrate(app, db)
    __add_default_course(app)

    # init api
    api.init_app(app)

    # init swagger
    app.register_blueprint(SWAGGER_UI_BLUEPRINT, url_prefix=SWAGGER_URL)

    return app

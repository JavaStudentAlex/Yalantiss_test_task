"""Module for initialising  flask application"""
from datetime import datetime
from os import environ

from flask import Flask
from flask_migrate import Migrate

from app.api import api
from app.models import Course, bcrypt, db
from app.swagger import SWAGGER_UI_BLUEPRINT, SWAGGER_URL


def __add_default_courses(app: Flask):
    app.app_context().push()
    db.create_all()
    if Course.query.count() == 0:

        course = Course(
            "course1",
            datetime.strptime("2021-01-01", "%Y-%m-%d").date(),
            datetime.strptime("2021-01-01", "%Y-%m-%d").date(),
            1,
        )
        db.session.add(course)

        course2 = Course(
            "course2",
            datetime.strptime("2019-01-01", "%Y-%m-%d").date(),
            datetime.strptime("2019-01-01", "%Y-%m-%d").date(),
            2,
        )
        db.session.add(course2)

        course3 = Course(
            "course3",
            datetime.strptime("2018-01-01", "%Y-%m-%d").date(),
            datetime.strptime("2018-01-01", "%Y-%m-%d").date(),
            3,
        )
        db.session.add(course3)

        db.session.commit()


def create_flask_app(config_object=None):
    """Flask app factory method"""
    app = Flask(__name__)
    if config_object is not None:
        app.config.from_object(config_object)
    else:
        app.config.from_mapping(
            BCRYPT_LOG_ROUNDS=10,
            SECRET_KEY=environ["FLASK_SECRET_KEY"],
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            SQLALCHEMY_DATABASE_URI=environ["DATABASE_PATH"],
        )

    # init database
    db.init_app(app)
    bcrypt.init_app(app)
    Migrate(app, db)
    __add_default_courses(app)

    # init api
    api.init_app(app)

    # init swagger
    app.register_blueprint(SWAGGER_UI_BLUEPRINT, url_prefix=SWAGGER_URL)

    return app

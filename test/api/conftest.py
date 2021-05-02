"""Module for testing api"""
from os import environ

import pytest
from py.path import local

from app import create_flask_app


@pytest.fixture(scope="function")
def database(tmpdir: local):

    database_dir = "database"
    database_file = "test_database.db"

    return tmpdir.mkdir(database_dir).join(database_file)


@pytest.fixture(scope="function")
def app(database: str):
    test_app = create_flask_app(
        {
            "BCRYPT_LOG_ROUNDS": 10,
            "SECRET_KEY": environ["FLASK_SECRET_KEY"],
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database}",
        }
    )
    return test_app

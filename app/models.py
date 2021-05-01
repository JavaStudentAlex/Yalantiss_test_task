from dataclasses import dataclass
from datetime import date

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import DeclarativeMeta

db = SQLAlchemy()
base_model: DeclarativeMeta = db.Model
bcrypt = Bcrypt()


@dataclass
class Course(base_model):
    id: int
    title: str
    start_date: date
    end_date: date
    classes_count: int

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    classes_count = db.Column(db.Integer)

    def __init__(self, title, start, finish, stdnt_number=0):
        self.title = title
        self.start_date = start
        self.end_date = finish
        self.classes_count = stdnt_number

from datetime import date
from typing import Tuple

from sqlalchemy import and_

from app.models import Course, db


def get_all_courses() -> Tuple:
    result = Course.query.all()
    return result


def get_course_by_id(course_id: int) -> Course:
    result = Course.query.filter_by(id=course_id).first()
    if result is None:
        raise KeyError()
    return result


def remove_course_by_id(course_id: int) -> None:
    course_to_remove = Course.query.filter_by(id=course_id).first()
    if course_to_remove is None:
        raise KeyError()
    db.session.delete(course_to_remove)
    db.session.commit()


def create_course(title: str, start: date, end: date, classes: int) -> None:
    course = Course(title, start, end, classes)
    db.session.add(course)
    db.session.commit()


def find_course_by_filters(title_contain, not_finish_till, not_start_after) -> Tuple:
    options = list()

    # add filter if the title filter set
    if title_contain is not None:
        # mypy does not find contains() dynamic method
        options.append(Course.title.contains(title_contain))  # type: ignore

    # add filter if the left date edge filter set
    if not_finish_till is not None:
        options.append(Course.end_date >= not_finish_till)

    # add filter if the right date edge filter set
    if not_start_after is not None:
        options.append(Course.start_date <= not_start_after)

    return Course.query.filter(and_(*options)).all()

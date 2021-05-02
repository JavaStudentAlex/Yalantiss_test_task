"""Module for testing api"""
from flask import url_for
from flask.testing import FlaskClient


def test_all_courses_available(client: FlaskClient):
    assert client.get(url_for("get_all_courses")).status_code == 200


def test_all_courses_right_entities_number(client: FlaskClient):
    assert len(client.get(url_for("get_all_courses")).json) == 3


def test_course_by_id_available(client: FlaskClient):
    assert client.get(url_for("get_course", id=1)).status_code == 200


def test_course_by_invalid_id(client: FlaskClient):
    assert client.get(url_for("get_course", id="text_id")).status_code == 400


def test_course_by_wrong_id(client: FlaskClient):
    assert client.get(url_for("get_course", id=10)).status_code == 400


def test_course_by_right_id(client: FlaskClient):
    assert client.get(url_for("get_course", id=1)).json["id"] == 1


def test_filter_courses_available(client: FlaskClient):
    assert client.get(url_for("filter_courses")).status_code == 200


def test_filter_courses_by_no_params(client: FlaskClient):
    response = client.get(url_for("filter_courses"))
    assert len(response.json) == 3


def test_filter_courses_invalid_left_border_date_format(client: FlaskClient):
    assert (
        client.get(
            url_for("filter_courses", not_finished_till="invalid_date")
        ).status_code
        == 400
    )


def test_filter_courses_invalid_right_border_date_format(client: FlaskClient):
    assert (
        client.get(
            url_for("filter_courses", not_start_after="invalid_date")
        ).status_code
        == 400
    )


def test_filter_courses_by_title(client: FlaskClient):
    assert client.get(url_for("filter_courses", title_contains="1")).json[0]["id"] == 1


def test_filter_courses_by_left_border_date(client: FlaskClient):
    assert (
        client.get(url_for("filter_courses", not_finished_till="2021-01-01")).json[0][
            "id"
        ]
        == 1
    )


def test_filter_courses_by_right_border_date(client: FlaskClient):
    assert (
        client.get(url_for("filter_courses", not_start_after="2021-01-01")).json[0][
            "id"
        ]
        == 1
    )


def test_filter_courses_by_title_contains_and_left_border(client: FlaskClient):
    response = client.get(
        url_for(
            "filter_courses", title_contains="course", not_finished_till="2020-01-01"
        )
    )
    assert len(response.json) == 1
    assert response.json[0]["id"] == 1


def test_filter_courses_by_title_contains_and_right_border(client: FlaskClient):
    response = client.get(
        url_for("filter_courses", title_contains="course", not_start_after="2018-01-01")
    )
    assert len(response.json) == 1
    assert response.json[0]["id"] == 3


def test_filter_courses_by_all_params(client: FlaskClient):
    response = client.get(
        url_for(
            "filter_courses",
            title_contains="course",
            not_finished_till="2020-01-01",
            not_start_after="2021-02-02",
        )
    )
    assert len(response.json) == 1
    assert response.json[0]["id"] == 1


def test_delete_course_by_no_params(client: FlaskClient):
    assert client.delete(url_for("delete_course")).status_code == 400


def test_delete_course_by_invalid_id(client: FlaskClient):
    assert client.delete(url_for("delete_course", id="invalid id")).status_code == 400


def test_delete_course_by_wrong_id(client: FlaskClient):
    assert client.delete(url_for("delete_course", id=10)).status_code == 400


def test_delete_course_by_right_id(client: FlaskClient):
    assert client.delete(url_for("delete_course", id=1)).status_code == 200
    assert len(client.get(url_for("get_all_courses")).json) == 2


def test_add_course_invalid_start_date(client: FlaskClient):
    args = {"start": "invalid_date"}
    assert client.post(url_for("add_course"), data=args).status_code == 400


def test_add_course_invalid_finish_date(client: FlaskClient):
    args = {"finish": "invalid_date"}
    assert client.post(url_for("add_course"), data=args).status_code == 400


def test_add_course_invalid_classes_number(client: FlaskClient):
    args = {"classes": "invalid_date"}
    assert client.post(url_for("add_course"), data=args).status_code == 400


def test_add_valid_course(client: FlaskClient):
    args = {
        "title": "course4",
        "start": "2020-03-03",
        "finish": "2020-04-04",
        "classes": 4,
    }
    assert client.post(url_for("add_course"), data=args).status_code == 200
    assert client.get(url_for("get_course", id=4)).json["id"] == 4

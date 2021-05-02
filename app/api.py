"""Rest API module"""
from datetime import datetime

from flask import jsonify
from flask_restful import Api, Resource, reqparse

from core.process_courses import (
    create_course,
    find_course_by_filters,
    get_all_courses,
    get_course_by_id,
    remove_course_by_id,
)


class AllCoursesApi(Resource):
    def get(self):
        """Handling get request of all courses"""
        return jsonify(get_all_courses())


class DetailCourseApi(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        "id", required=True, type=int, help="course id should be set as integer"
    )

    def get(self):
        """Handling get request of course by id"""
        args = self.parser.parse_args()
        course_id = args.id
        try:
            return jsonify(get_course_by_id(course_id))
        except KeyError:
            return {"message": {"id": "Wrong course id"}}, 400
        except Exception:
            return {"message": {"database": "Sorry, error with database"}}, 400


class DeleteCourse(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        "id", required=True, type=int, help="course id should be integer"
    )

    def delete(self):
        """Handling delete request of course by id"""
        args = self.parser.parse_args()
        course_id = args.id
        try:
            remove_course_by_id(course_id)
            return {"message": "Course deleted"}, 200
        except KeyError:
            return {"message": {"id": "Wrong course id"}}, 400
        except Exception:
            return {"message": {"database": "Sorry, error with database"}}, 400


class AddCourse(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("title", required=True, type=str)
    parser.add_argument(
        "start",
        required=True,
        type=lambda x: datetime.strptime(x, "%Y-%m-%d").date(),
        help="Date has to be in defined format",
    )
    parser.add_argument(
        "finish",
        required=True,
        type=lambda x: datetime.strptime(x, "%Y-%m-%d").date(),
        help="Date has to be in defined format",
    )
    parser.add_argument(
        "classes", required=True, type=int, help="Number of classes should be integer"
    )

    def post(self):
        """Handling adding course"""
        args = self.parser.parse_args()
        title, start, end, classes = args.title, args.start, args.finish, args.classes

        if start > end:
            return {
                "message": {"start_date-finish_date": "Start can not be later than end"}
            }, 400

        if classes < 0:
            return {
                "message": {
                    "classes": "Course participants number"
                    " can not be greater less than 0"
                }
            }, 400
        try:
            create_course(title, start, end, classes)
            return {"message": "Course added"}, 200
        except Exception:
            return {"message": {"database": "Sorry, error with database"}}, 400


class FilterCourses(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("title_contains", type=str)
    parser.add_argument(
        "not_finished_till",
        type=lambda x: datetime.strptime(x, "%Y-%m-%d").date(),
        help="Date has to be in defined format",
    )
    parser.add_argument(
        "not_start_after",
        type=lambda x: datetime.strptime(x, "%Y-%m-%d").date(),
        help="Date has to be in defined format",
    )

    def get(self):
        """Handling get request by filtering by name and dates"""
        args = self.parser.parse_args()
        title_contains = args.title_contains
        not_finished_till = args.not_finished_till
        not_start_after = args.not_start_after

        if not_finished_till is not None and not_start_after is not None:
            if not_finished_till > not_start_after:
                return {
                    "message": {"time ": "Start date filter has to be earlier"}
                }, 400

        return jsonify(
            find_course_by_filters(title_contains, not_finished_till, not_start_after)
        )


api = Api()
api.add_resource(AllCoursesApi, "/api/get_all_courses", endpoint="get_all_courses")
api.add_resource(DetailCourseApi, "/api/get_course", endpoint="get_course")
api.add_resource(DeleteCourse, "/api/delete_course", endpoint="delete_course")
api.add_resource(AddCourse, "/api/add_course", endpoint="add_course")
api.add_resource(FilterCourses, "/api/filter_courses", endpoint="filter_courses")

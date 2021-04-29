"""Rest API module"""
from flask_restful import Api, Resource


class AllCoursesApi(Resource):
    def get(self):
        """Handling get request of all courses"""
        return "All courses"


class DetailCourseApi(Resource):
    def get(self):
        """Handling get request of course by id"""
        return "Just one course"


class DeleteCourse(Resource):
    def delete(self):
        """Handling delete request of course by id"""
        return "Just one course deleted"


class AddCourse(Resource):
    def post(self):
        """Handling adding course"""
        return "Added course"


class FilterCourses(Resource):
    def get(self):
        """Handling get request by filtering by name and dates"""


api = Api()
api.add_resource(AllCoursesApi, "/api/get_all_courses")
api.add_resource(DetailCourseApi, "/api/get_course")
api.add_resource(DeleteCourse, "/api/delete_course")
api.add_resource(AddCourse, "/api/add_course")
api.add_resource(FilterCourses, "/api/filter_courses")

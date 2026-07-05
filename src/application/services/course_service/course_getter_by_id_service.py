
from typing import Optional

from src.domain.entities.course import Course
from src.domain.repository_contract.course_repository_contract import CourseRepositoryContract
from src.application.services_contract.course_contract.course_getter_by_id_contract import CourseGetterByIdContract


class CourseGetterByIdService(CourseGetterByIdContract):
    def __init__(self, course_repository:CourseRepositoryContract):
        self._repository = course_repository

    def get_course_by_id(self, course: Course) -> Optional[Course]:
        try:
            return self._repository.get_course_by_id(course.course_id)
        except Exception as e:
            print(f"Error occurred while fetching course by ID: {e}")
            return None
from typing import List

from src.domain.entities.course import Course
from src.domain.repository_contract.course_repository_contract import CourseRepositoryContract
from src.application.services_contract.course_contract.course_getter_contract import CourseGetterContract

class CourseGetterService(CourseGetterContract):
    def __init__(self, course_repository: CourseRepositoryContract):
        self._repository = course_repository

    def get_all_courses(self) -> List[Course]:
        try:
            return self._repository.get_all_courses()
        except Exception as e:
            print(f"Error occurred while fetching all courses: {e}")
            return []
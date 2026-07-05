from typing import List

from src.domain.entities.course import Course
from src.domain.repository_contract.course_repository_contract import CourseRepositoryContract

from src.infrastructure.db_context.db_context import Context

class CourseRepository(CourseRepositoryContract):

    def __init__(self,context:Context):
        self._context = context
    
    def add_course(self, course: Course) -> bool:
        try:
            self._context.save_entity(course.to_csv())
            return True
        except Exception as e:
            print(f"Error adding course: {e}")
            return False

    def get_course_by_id(self, course_id: str) -> Course:
        try:
            file_reader = self._context.get_all_entities()
            for line in file_reader:
                if line.startswith(course_id):
                    return Course.from_csv(line)
            return None
        except Exception as e:
            print(f"Error retrieving course: {e}")
            return None

    def get_all_courses(self) -> List[Course]:
        courses = []
        try:
            file_reader = self._context.get_all_entities()
            for line in file_reader:
                courses.append(Course.from_csv(line))
            return courses
        except Exception as e:
            print(f"Error retrieving all courses: {e}")
            return []

    def update_course(self, updated_course: Course) -> bool:
        try:
            self._context.update_entity(updated_course.to_csv(), updated_course.course_id)
            return True
        except Exception as e:
            print(f"Error updating course: {e}")
            return False

    def remove_course(self, course_id: str) -> bool:
        try:
            self._context.remove_entity(course_id)
            return True
        except Exception as e:
            print(f"Error removing course: {e}")
            return False    
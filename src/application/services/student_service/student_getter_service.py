
from typing import List

from src.domain.entities.student import Student
from src.domain.repository_contract.course_repository_contract import CourseRepositoryContract
from src.domain.repository_contract.student_repository_contract import StudentRepositoryContract
from src.application.services_contract.student_contract.student_getter_contract import StudentGetterContract
from src.application.DTO.student_with_courses_dto import StudentWithCoursesDTO

class StudentGetterService(StudentGetterContract):
    def __init__(self, student_repository: StudentRepositoryContract,course_repository:CourseRepositoryContract):
        self._student_repository = student_repository
        self._course_repository = course_repository

    def get_all_students(self) -> List[Student]:
        """
        Recupera todos os estudantes.
        Retorna uma lista de objetos Student.
        """
        try:
            students = self._student_repository.get_all_students()
            courses = self._course_repository.get_all_courses()
            students_dto = StudentWithCoursesDTO.from_students_and_courses(students,courses)
            return students_dto
        except Exception as e:
            print(f"Error retrieving students: {e}")
            return []
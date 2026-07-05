from typing import Optional

from src.domain.entities.student import Student
from src.domain.repository_contract.student_repository_contract import StudentRepositoryContract
from src.domain.repository_contract.course_repository_contract import CourseRepositoryContract
from src.application.services_contract.student_contract.student_getter_by_id_contract import StudentGetterByIdContract
from src.application.DTO.student_with_courses_dto import StudentWithCoursesDTO

class StudentGetterByIdService(StudentGetterByIdContract):
    def __init__(self, student_repository: StudentRepositoryContract,course_repository:CourseRepositoryContract):
        self._student_repository = student_repository
        self._course_repository = course_repository

    def get_student_by_id(self, student: Student)-> Optional[Student]:
        """
        Recupera um estudante pelo ID.
        Retorna o objeto Student se encontrado, None caso contrário.
        """
        try:
            student = self._student_repository.get_student_by_id(student_id=student.student_id)
            courses = self._course_repository.get_all_courses()
            student_dto = StudentWithCoursesDTO.from_student_and_courses(student,courses)
            return student_dto
        except Exception as e:
            print(f"Error retrieving student by ID: {e}")
            return None
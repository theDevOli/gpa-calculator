from typing import List
import re

from src.domain.entities.course import Course
from src.domain.entities.student import Student

class StudentWithCoursesDTO:
    _TOKEN = object()

    def __init__(self, token, student: Student, courses: List[Course]):
        """O construtor agora exige o token privado, impedindo a instanciação direta tradicional."""
        if token is not self._TOKEN:
            raise ValueError(
                "Para instanciar esta classe, utilize o método de fábrica: "
                "StudentWithCoursesDTO.from_student_and_courses(student, courses)"
            )
        
        self.student = student
        self.courses = courses
    
    @property
    def name(self) -> str:
        """Atalho para ler o nome do estudante direto na raiz do DTO."""
        return self.student.name

    @property
    def student_id(self) -> str:
        """Atalho para ler o ID do estudante direto na raiz do DTO."""
        return self.student.student_id

    @property
    def student_tax_id(self) -> str:
        """Atalho para ler o CPF do estudante direto na raiz do DTO."""
        return re.sub(r"(\d{3})(\d{3})(\d{3})(\d{2})", r"\1.\2.\3-\4", self.student.student_tax_id)
    
    @property
    def gpa(self)->float:
        gpa_value = Course.calculate_gpa(self.courses)
        return round(gpa_value, 2)
    
    @property
    def ira(self)->float:
        ira_value = Course.calculate_ira(self.courses)
        return round(ira_value, 2)

    @classmethod
    def from_student_and_courses(cls, student: Student, courses: List[Course]) -> "StudentWithCoursesDTO":
        """Método de fábrica oficial para instanciar e filtrar o DTO."""
        courses_id = student.courses

        filtered_courses = list(filter(lambda c: c.course_id in courses_id, courses))
        sorted_courses = sorted(filtered_courses, key=lambda c: c.name)

        return cls(cls._TOKEN, student, sorted_courses)
    
    @classmethod
    def from_students_and_courses(cls, students: List[Student], courses: List[Course]) -> "StudentWithCoursesDTO":
        """Método de fábrica oficial para instanciar e filtrar o DTO."""
        students_dto = []

        sorted_students = sorted(students, key=lambda c: c.name)

        for student in sorted_students:
            dto = cls.from_student_and_courses(student,courses)
            students_dto.append(dto)

        return students_dto
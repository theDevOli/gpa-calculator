
from src.domain.entities.course import Course
from src.domain.repository_contract.course_repository_contract import CourseRepositoryContract
from src.domain.repository_contract.student_repository_contract import StudentRepositoryContract
from src.application.services_contract.course_contract.course_adder_contract import CourseAdderContract

class CourseAdderService(CourseAdderContract):
    def __init__(self, course_repository: CourseRepositoryContract,student_repository:StudentRepositoryContract):
        self._course_repository = course_repository
        self._student_repository = student_repository

    def add_course(self, student_id:str, new_course: Course) -> str:
        try:
            student_db = self._student_repository.get_student_by_id(student_id=str(student_id))
            if student_db is None: 
                return 'Nao foi possivel encontrar o estudante para adicionar o curso.'

            student_courses = self._course_repository.get_courses_by_ids(student_db.courses)
            course_exists = any(course.name == new_course.name for course in student_courses)
            if course_exists: 
                return 'Curso já existe para este estudante.'
            
            wasAdded = self._course_repository.add_course(new_course)
            if not wasAdded: 
                return 'Nao foi possivel adicionar o curso.'

            student_db.add_course(new_course.course_id)
            wasUpdated = self._student_repository.update_student(student_db)
            if not wasUpdated: 
                return 'Nao foi possivel atualizar o estudante.'

            return "Curso adicionado com sucesso."
        except Exception as e:
            print(f"Error adding course: {e}")
            return "Erro ao adicionar curso"
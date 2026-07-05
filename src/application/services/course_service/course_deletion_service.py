from src.domain.entities.course import Course
from src.domain.repository_contract.course_repository_contract import CourseRepositoryContract
from src.domain.repository_contract.student_repository_contract import StudentRepositoryContract
from src.application.services_contract.course_contract.course_deletion_contract import CourseDeletionContract


class CourseDeletionService(CourseDeletionContract):
    def __init__(self, course_repository:CourseRepositoryContract, student_repository:StudentRepositoryContract):
        self._course_repository = course_repository
        self._student_repository = student_repository

    def delete_course(self, student_id, course:Course) -> str:
        try:
            student_db = self._student_repository.get_student_by_id(student_id=student_id)
            if student_db is None: 
                return 'Nao foi possivel encontrar o estudante para deletar o curso.'

            student_db.remove_course(course_id=course.course_id)
            isUpdated = self._student_repository.update_student(student_db)
            if not isUpdated: 
                return 'Nao foi possivel atualizar o estudante.'
            
            courses = self._course_repository.get_all_courses()
            filtered_courses = list(filter(lambda c: c.course_id == course.course_id, courses))

            if len(filtered_courses) == 0:
                return 'Curso nao encontrado.'

            
            was_removed = self._course_repository.remove_course(course.course_id)
            if not was_removed:
                return 'Nao foi possivel remover o curso.'
            
            return 'Curso deletado com sucesso.'
        except Exception as e:
            print(f"Error deleting course: {e}")
            return "Erro ao deletar curso"
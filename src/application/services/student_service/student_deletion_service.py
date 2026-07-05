from src.domain.entities.student import Student
from src.domain.repository_contract.student_repository_contract import StudentRepositoryContract
from src.domain.repository_contract.course_repository_contract import CourseRepositoryContract
from src.application.services_contract.student_contract.student_deletion_contract import StudentDeletionContract


class StudentDeletionService(StudentDeletionContract):
    def __init__(self, student_repository: StudentRepositoryContract,course_repository:CourseRepositoryContract):
        self._student_repository = student_repository
        self._course_repository = course_repository

    def delete_student(self, student: Student) -> str:
        """Deleta um estudante.
        Retorna 'sucesso' se for bem-sucedido, 'Erro ao deletar estudante' caso contrário.
        """
        try:
            student_db = self._student_repository.get_student_by_id(student.student_id)

            if student_db is None:
                return 'Estudante não encontrado.'
            
            courses_id = student_db.courses
            for course_id in courses_id:
                self._course_repository.remove_course(course_id=course_id)
            
            was_removed = self._student_repository.remove_student(student.student_id)
            if not was_removed:
                return 'Nao foi possivel deletar o estudante.'
            
            return 'Sucesso ao deletar estudante.'
        except Exception as e:
            print(f"Error deleting student: {e}")
            return "Erro ao deletar estudante"
from src.domain.entities.student import Student
from src.domain.repository_contract.student_repository_contract import StudentRepositoryContract
from src.application.services_contract.student_contract.student_updatable_contract import StudentUpdatableContract

class StudentUpdatableService(StudentUpdatableContract):
    def __init__(self, student_repository: StudentRepositoryContract):
        self._repository = student_repository

    def update_student(self, student_to_update: Student) -> str:
        try:
            student_id = student_to_update.student_id

            db_student = self._repository.get_student_by_id(student_id)
            if db_student is None:
                return "Estudante não encontrado."
            
            was_updated = self._repository.update_student(student_to_update)
            if not was_updated:
                return "Nao foi possivel atualizar o estudante."
            
            return "Sucesso ao atualizar estudante."
        except Exception as e:
            print(f"Error updating student by ID: {e}")
            return "Erro ao atualizar estudante"
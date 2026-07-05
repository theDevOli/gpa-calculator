from src.domain.entities.student import Student
from src.domain.repository_contract.student_repository_contract import StudentRepositoryContract
from src.application.services_contract.student_contract.student_adder_contract import StudentAdderContract

class StudentAdderService(StudentAdderContract):
    def __init__(self, student_repository:StudentRepositoryContract):
        self._repository = student_repository
    def add_student(self, student: Student) -> str:
        """
        Salva um novo estudante no mecanismo de persistência.
        Retorna 'sucesso' se for bem-sucedido, 'Erro ao adicionar estudante' caso contrário.
        """
        try:
            student_db = self._repository.get_student_by_tax_id(student.student_tax_id)
            if student_db is not None:
                return 'Estudante já existe.'
            
            was_added = self._repository.add_student(student)
            if not was_added:
                return 'Nao foi possivel adicionar o estudante.'
            
            return 'Sucesso ao adicionar estudante.'
        except Exception as e:
            print(f"Error adding student: {e}")
            return "Erro ao adicionar estudante"
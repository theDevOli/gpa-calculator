from abc import ABC, abstractmethod

from src.domain.entities.student import Student

class StudentUpdatableContract(ABC):

    @abstractmethod
    def update_student(self, student_to_update: Student) -> str:
        """Atualiza os dados de um estudante.
        Retorna uma mensagem de sucesso ou erro.
        """
        pass
from abc import ABC, abstractmethod

from src.domain.entities.student import Student

class StudentDeletionContract(ABC):
    @abstractmethod
    def delete_student(self, student: Student) -> str:
        """Deleta um estudante.
        Retorna uma mensagem de sucesso ou erro.
        """
        pass
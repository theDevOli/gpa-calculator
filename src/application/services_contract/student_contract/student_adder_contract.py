from abc import ABC, abstractmethod

from src.domain.entities.student import Student

class StudentAdderContract(ABC):

    @abstractmethod
    def add_student(self, student: Student) -> str:
        """Salva um novo estudante no mecanismo de persistência. 
        Retorna uma mensagem de sucesso ou erro.
        """
        pass
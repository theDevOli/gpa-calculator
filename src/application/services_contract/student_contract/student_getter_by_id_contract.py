from abc import ABC, abstractmethod

from src.domain.entities.student import Student

class StudentGetterByIdContract(ABC):

    @abstractmethod
    def get_student_by_id(self, student: Student) -> Student:
        """Recupera um estudante pelo ID.
        Retorna o objeto Student se encontrado, None caso contrário.
        """
        pass
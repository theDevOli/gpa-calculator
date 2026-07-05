from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.student import Student
class StudentRepositoryContract(ABC):

    @abstractmethod
    def add_student(self, student: Student) -> bool:
        """Salva ou atualiza um estudante no mecanismo de persistência."""
        pass

    @abstractmethod
    def get_student_by_id(self, student_id: str) -> Optional[Student]:
        """Busca um estudante pelo seu ID único. Retorna None se não encontrar."""
        pass

    @abstractmethod
    def get_student_by_tax_id(self, student_tax_id: str) -> Optional[Student]:
        """Busca um estudante pelo seu CPF. Retorna None se não encontrar."""
        pass

    @abstractmethod
    def get_all_students(self) -> list[Student]:
        """Retorna todos os estudantes."""
        pass

    @abstractmethod
    def update_student(self,updated_student: Student) -> bool:
        """Atualiza as informações de um estudante."""
        pass

    @abstractmethod
    def remove_student(self, student_id: str) -> bool:
        """Remove um estudante do mecanismo de persistência."""
        pass
from abc import ABC, abstractmethod
from typing import List

from src.domain.entities.student import Student

class StudentGetterContract(ABC):

    @abstractmethod
    def get_all_students(self) -> List[Student]:
        """Recupera todos os estudantes.
        Retorna uma lista de objetos Student.
        """
        pass
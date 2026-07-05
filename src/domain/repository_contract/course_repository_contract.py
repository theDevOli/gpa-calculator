from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.course import Course

class CourseRepositoryContract(ABC):

    @abstractmethod
    def add_course(self, course: Course) -> bool:
        """Salva um novo curso no mecanismo de persistência. 
        Retorna True se for bem-sucedido, False caso contrário.
        """
        pass

    @abstractmethod
    def get_course_by_id(self, course_id: str) -> Optional[Course]:
        """Busca um curso pelo seu ID único. 
        Retorna o objeto Course ou None se não for encontrado.
        """
        pass

    @abstractmethod
    def get_all_courses(self) -> list[Course]:
        """Retorna uma lista com todos os cursos cadastrados."""
        pass

    @abstractmethod
    def update_course(self, updated_course: Course) -> bool:
        """Atualiza as informações de um curso existente.
        Retorna True se a atualização ocorrer com sucesso.
        """
        pass

    @abstractmethod
    def remove_course(self, course_id: str) -> bool:
        """Remove um curso do mecanismo de persistência com base no ID.
        Retorna True se for removido com sucesso.
        """
        pass
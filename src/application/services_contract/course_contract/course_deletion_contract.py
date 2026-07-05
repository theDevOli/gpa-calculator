from abc import ABC, abstractmethod

from src.domain.entities.course import Course

class CourseDeletionContract(ABC):
    @abstractmethod
    def delete_course(self, student_id:str, course:Course)-> str:
        pass
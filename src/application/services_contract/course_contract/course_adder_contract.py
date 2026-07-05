from abc import ABC, abstractmethod

from src.domain.entities.course import Course

class CourseAdderContract(ABC):
    @abstractmethod
    def add_course(self,student_id:str, new_course:Course)-> str:
        pass
from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.course import Course

class CourseGetterContract(ABC):
    @abstractmethod
    def get_all_courses(self) -> List[Course]:
        pass
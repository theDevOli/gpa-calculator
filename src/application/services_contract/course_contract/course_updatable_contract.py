from abc import ABC, abstractmethod

from src.domain.entities.course import Course

class CourseUpdatableContract(ABC):
    @abstractmethod
    def update_course(self, to_update_course: Course) -> str:
        pass
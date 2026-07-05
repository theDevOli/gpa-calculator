from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.course import Course

class CourseGetterByIdContract(ABC):
    @abstractmethod
    def get_course_by_id(self, course:Course)->Optional[Course]:
        pass
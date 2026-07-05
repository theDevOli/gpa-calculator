import uuid
import re

from src.domain.entities.course import Course

class Student:
    def __init__(self, name: str, student_tax_id:str, student_id: str = None, courses: list = None):
        self.student_id = student_id if student_id else str(uuid.uuid4())
        self.name = name
        self.student_tax_id = self.student_tax_id = re.sub(r"\D", "", str(student_tax_id))
        self.courses = courses if courses is not None else []
    
    def to_csv(self):
        if len(self.courses) == 0:
            return f"{self.student_id},{self.name},{self.student_tax_id}"
        
        courses_str = ';'.join(self.courses)
        return f"{self.student_id},{self.name},{self.student_tax_id},{courses_str}"
    
    def to_dict(self):
        return {
            "studentId": self.student_id,
            "name": self.name,
            "studentTaxId": self.student_tax_id,
            "courses": self.courses
        }
    
    @classmethod
    def from_csv(cls, csv_data: str):
        parts = csv_data.strip().split(',')
        student_id = parts[0]
        name = parts[1]
        student_tax_id = parts[2]
        courses = parts[3].split(';') if len(parts) > 3 else []
        student = cls(name, student_tax_id, student_id, courses)
        return student

    def add_course(self, course_id):
        self.courses.append(course_id)
    
    def remove_course(self,course_id):
        if course_id in self.courses:
            self.courses.remove(course_id)
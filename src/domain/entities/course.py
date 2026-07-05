import uuid

class Course:
    def __init__(self, name: str, credit_hours: int, grade: float, course_id: str = None):
        self.course_id = course_id if course_id else str(uuid.uuid4())
        self.name = name
        self.credit_hours = credit_hours
        if grade < 0 or grade > 10:
            raise ValueError("O valor da nota deve estar entre 0 e 10.")
        self.grade = grade

    def to_csv(self):
        return f"{self.course_id},{self.name},{self.credit_hours},{self.grade}"

    @classmethod
    def from_csv(cls, csv_data: str):
        parts = csv_data.strip().split(',')

        return cls(
            name=parts[1],
            credit_hours=int(parts[2]),
            grade=float(parts[3]),
            course_id=parts[0]
        )
    
    @staticmethod
    def _convert_brazil_to_us_points(grade: float) -> float:
        """Converte a nota brasileira (0-10) para os pontos do GPA americano (0.0-4.0)"""
        if grade >= 9.0:
            return 4.0  # A
        elif grade >= 7.0:
            return 3.0  # B
        elif grade >= 5.0:
            return 2.0  # C
        elif grade >= 3.0:
            return 1.0  # D
        else:
            return 0.0  # F
        
    @staticmethod
    def calculate_gpa(courses: list) -> float:
        """Calcula o GPA americano ponderado com base na lista de cursos brasileiros"""
        total_points = 0
        total_credits = 0

        for course in courses:
            us_points = Course._convert_brazil_to_us_points(course.grade)

            total_points += us_points * course.credit_hours
            total_credits += course.credit_hours

        if total_credits == 0:
            return 0.0

        # 3. Retorna a média final ponderada
        return round(total_points / total_credits, 2)

    @staticmethod
    def calculate_ira(courses: list):
        total_points = 0
        total_credits = 0

        for course in courses:
            total_points += course.grade * course.credit_hours
            total_credits += course.credit_hours

        if total_credits == 0:
            return 0

        return total_points / total_credits
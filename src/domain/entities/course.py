import uuid

class Course:
    """Representa a entidade de um Curso (ou Disciplina) no domínio acadêmico.

    Esta classe armazena os dados individuais de uma disciplina cursada por um estudante,
    como nome, carga horária e nota. Também provê métodos utilitários para serialização
    em formato CSV e cálculo de índices acadêmicos (GPA americano e IRA brasileiro).

    Attributes:
        course_id (str): Identificador único do curso (gerado automaticamente via UUID4 caso não fornecido).
        name (str): Nome da disciplina/curso.
        credit_hours (int): Carga horária ou número de créditos da disciplina.
        grade (float): Nota final obtida no curso (deve estar contida no intervalo de 0 a 10).
    """

    def __init__(self, name: str, credit_hours: int, grade: float, course_id: str = None):
        """Inicializa uma instância da entidade Course.

        Args:
            name (str): Nome da disciplina.
            credit_hours (int): Carga horária ou créditos atribuídos à disciplina.
            grade (float): Nota final do aluno na disciplina (escala de 0.0 a 10.0).
            course_id (str, optional): ID do curso. Se omitido, um UUID4 será gerado.

        Raises:
            ValueError: Se a nota fornecida não estiver no intervalo entre 0 e 10.
        """
        self.course_id = course_id if course_id else str(uuid.uuid4())
        self.name = name
        self.credit_hours = credit_hours
        if grade < 0 or grade > 10:
            raise ValueError("O valor da nota deve estar entre 0 e 10.")
        self.grade = grade

    def to_csv(self) -> str:
        """Serializa os dados do curso em uma linha no formato CSV.

        Returns:
            str: String formatada com os valores separados por vírgula no padrão:
                 "course_id,name,credit_hours,grade"
        """
        return f"{self.course_id},{self.name},{self.credit_hours},{self.grade}"

    @classmethod
    def from_csv(cls, csv_data: str):
        """Cria uma nova instância de Course a partir de uma string no formato CSV.

        Args:
            csv_data (str): Uma linha de texto contendo os dados do curso separados por vírgula.

        Returns:
            Course: Uma nova instância da classe Course populada com os dados do CSV.
        """
        parts = csv_data.strip().split(',')

        return cls(
            name=parts[1],
            credit_hours=int(parts[2]),
            grade=float(parts[3]),
            course_id=parts[0]
        )
    
    @staticmethod
    def _convert_brazil_to_us_points(grade: float) -> float:
        """Converte a nota brasileira (escala 0-10) para pontos equivalentes do GPA americano (escala 0.0-4.0).

        A conversão segue a seguinte regra de faixas:
        - Nota >= 9.0 -> 4.0 (Conceito A)
        - Nota >= 7.0 -> 3.0 (Conceito B)
        - Nota >= 5.0 -> 2.0 (Conceito C)
        - Nota >= 3.0 -> 1.0 (Conceito D)
        - Nota < 3.0  -> 0.0 (Conceito F)

        Args:
            grade (float): A nota do sistema brasileiro (0 a 10).

        Returns:
            float: A pontuação equivalente no sistema americano de GPA (0.0 a 4.0).
        """
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
        """Calcula o Grade Point Average (GPA) americano ponderado com base em uma lista de cursos.

        O GPA é calculado convertendo a nota de cada curso para a escala de 4.0 pontos,
        multiplicando-a pela carga horária (créditos) do curso, somando os resultados
        e dividindo pelo total de créditos acumulados.

        Args:
            courses (list[Course]): Lista de instâncias da entidade Course.

        Returns:
            float: O valor do GPA final arredondado para duas casas decimais. Retorna 0.0
                   se a soma total de créditos dos cursos for zero.
        """
        total_points = 0
        total_credits = 0

        for course in courses:
            us_points = Course._convert_brazil_to_us_points(course.grade)

            total_points += us_points * course.credit_hours
            total_credits += course.credit_hours

        if total_credits == 0:
            return 0.0

        return round(total_points / total_credits, 2)

    @staticmethod
    def calculate_ira(courses: list) -> float:
        """Calcula o Índice de Rendimento Acadêmico (IRA) ponderado com base em uma lista de cursos.

        O cálculo realiza a média ponderada utilizando a nota original brasileira (0 a 10)
        multiplicada pela respectiva carga horária de cada curso.

        Args:
            courses (list[Course]): Lista de instâncias da entidade Course.

        Returns:
            float: O valor do IRA ponderado. Retorna 0 se a soma total de créditos 
                   dos cursos for zero.
        """
        total_points = 0
        total_credits = 0

        for course in courses:
            total_points += course.grade * course.credit_hours
            total_credits += course.credit_hours

        if total_credits == 0:
            return 0

        return total_points / total_credits
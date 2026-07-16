import uuid
import re

from src.domain.entities.course import Course

class Student:
    """Representa a entidade de um Estudante no domínio acadêmico.

    Esta classe armazena os dados cadastrais do estudante, incluindo o seu registro de
    identificação fiscal (CPF/Tax ID) devidamente limpo (somente números) e a lista 
    dos identificadores dos cursos aos quais está associado. Também fornece métodos utilitários
    para serialização em formatos de dicionário e CSV.

    Attributes:
        student_id (str): Identificador único do estudante (gerado automaticamente via UUID4 caso não fornecido).
        name (str): Nome completo do estudante.
        student_tax_id (str): Registro fiscal (CPF ou Tax ID) contendo apenas caracteres numéricos.
        courses (list[str]): Lista contendo os IDs (`course_id`) dos cursos associados ao estudante.
    """

    def __init__(self, name: str, student_tax_id: str, student_id: str = None, courses: list = None):
        """Inicializa uma nova instância da entidade Student.

        Args:
            name (str): Nome do estudante.
            student_tax_id (str): Registro fiscal (CPF ou equivalente) do estudante (pode conter pontuação).
            student_id (str, optional): Identificador do estudante. Se omitido, um UUID4 será gerado.
            courses (list[str], optional): Lista inicial de IDs de cursos associados. Se omitida, inicia vazia.
        """
        self.student_id = student_id if student_id else str(uuid.uuid4())
        self.name = name
        self.student_tax_id = re.sub(r"\D", "", str(student_tax_id))
        self.courses = courses if courses is not None else []
    
    def to_csv(self) -> str:
        """Serializa os dados do estudante em uma linha no formato CSV.

        Se o estudante possuir cursos, as referências de IDs de cursos serão 
        unidas usando o caractere ponto e vírgula (`;`) como delimitador interno.

        Returns:
            str: String formatada com os valores separados por vírgula no padrão:
                 - Sem cursos: "student_id,name,student_tax_id"
                 - Com cursos: "student_id,name,student_tax_id,course_id1;course_id2;..."
        """
        if len(self.courses) == 0:
            return f"{self.student_id},{self.name},{self.student_tax_id}"
        
        courses_str = ';'.join(self.courses)
        return f"{self.student_id},{self.name},{self.student_tax_id},{courses_str}"
    
    def to_dict(self) -> dict:
        """Converte as propriedades do estudante para um dicionário (estrutura chave-valor).

        Geralmente utilizado para facilitar a serialização em formato JSON ou o mapeamento
        em camadas de transporte de dados (DTOs).

        Returns:
            dict: Dicionário contendo as chaves 'studentId', 'name', 'studentTaxId' e 'courses'.
        """
        return {
            "studentId": self.student_id,
            "name": self.name,
            "studentTaxId": self.student_tax_id,
            "courses": self.courses
        }
    
    @classmethod
    def from_csv(cls, csv_data: str):
        """Cria uma nova instância de Student a partir de uma string de dados no formato CSV.

        Args:
            csv_data (str): Uma linha de texto representando os dados do estudante no formato CSV.

        Returns:
            Student: Uma nova instância da classe Student populada com os dados extraídos do CSV.
        """
        parts = csv_data.strip().split(',')
        student_id = parts[0]
        name = parts[1]
        student_tax_id = parts[2]
        courses = parts[3].split(';') if len(parts) > 3 else []
        student = cls(name, student_tax_id, student_id, courses)
        return student

    def add_course(self, course_id: str) -> None:
        """Adiciona uma referência de ID de curso à lista de cursos do estudante.

        Args:
            course_id (str): O identificador único do curso que será vinculado.
        """
        self.courses.append(course_id)
    
    def remove_course(self, course_id: str) -> None:
        """Remove a referência de um ID de curso específico da lista do estudante, se existir.

        Args:
            course_id (str): O identificador único do curso a ser desvinculado.
        """
        if course_id in self.courses:
            self.courses.remove(course_id)
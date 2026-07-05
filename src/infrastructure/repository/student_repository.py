from typing import Optional, List
from src.domain.entities.student import Student
from src.domain.repository_contract.student_repository_contract import StudentRepositoryContract
from src.infrastructure.db_context.db_context import Context

class StudentRepository(StudentRepositoryContract):
    """Repositório responsável por gerenciar a persistência dos dados de estudantes.

    Esta classe implementa o contrato `StudentRepositoryContract` e faz a ponte 
    entre a camada de domínio e o mecanismo de persistência em arquivos CSV, 
    utilizando Injeção de Dependência para manipulação do banco de dados (Context).
    """

    def __init__(self, context: Context):
        """Inicializa o repositório com um contexto de persistência injetado.

        Args:
            context (Context): O contexto de banco de dados/infraestrutura 
                               responsável pela leitura e escrita no arquivo físico.
        """
        self._context = context

    def add_student(self, student: Student) -> bool:
        """Salva um novo estudante no arquivo de dados.

        Args:
            student (Student): O objeto entidade do estudante a ser salvo.

        Returns:
            bool: True se o estudante foi adicionado com sucesso, False em caso de erro.
        """
        try:
            self._context.save_entity(student.to_csv())
            return True
        except Exception as e:
            print(f"Error adding student: {e}")
            return False

    def get_student_by_id(self, student_id: str) -> Optional[Student]:
        """Busca um estudante pelo seu identificador único (UUID).

        Args:
            student_id (str): O ID do estudante no formato string UUID.

        Returns:
            Optional[Student]: O objeto Student se encontrado, ou None se não existir.
        """
        try:
            file_reader = self._context.get_all_entities()
            for line in file_reader:
                if line.strip().startswith(student_id):
                    return Student.from_csv(line)
            return None
        except Exception as e:
            print(f"Error retrieving student: {e}")
            return None
    
    def get_student_by_tax_id(self, student_tax_id: str) -> Optional[Student]:
        """Busca um estudante no sistema através do seu CPF (student_tax_id).

        Args:
            student_tax_id (str): O CPF do estudante obtido para busca.

        Returns:
            Optional[Student]: O objeto Student correspondente, ou None se não encontrado.
        """
        try:
            file_reader = self._context.get_all_entities()
            for line in file_reader:
                if not line.strip():
                    continue

                data = line.strip().split(',')

                if len(data) >= 3 and data[2] == student_tax_id:
                    return Student.from_csv(line)
            return None
        except Exception as e:
            print(f"Error retrieving student by tax ID: {e}")
            return None

    def get_all_students(self) -> List[Student]:
        """Recupera todos os estudantes armazenados no arquivo de persistência.

        Returns:
            List[Student]: Uma lista contendo objetos instanciados de todos os 
                           estudantes válidos encontrados. Retorna uma lista vazia 
                           caso ocorra erro ou o arquivo esteja sem dados.
        """
        students = []
        try:
            file_reader = self._context.get_all_entities()
            for line in file_reader:
                if line.strip():
                    students.append(Student.from_csv(line))
            return students
        except Exception as e:
            print(f"Error retrieving all students: {e}")
            return []
    
    def update_student(self, updated_student: Student) -> bool:
        """Atualiza os dados cadastrais de um estudante existente.

        Args:
            updated_student (Student): O objeto Student contendo os novos dados 
                                       e o ID original a ser localizado.

        Returns:
            bool: True se a atualização foi concluída com sucesso, False caso contrário.
        """
        try:
            print(updated_student)
            self._context.update_entity(updated_student.to_csv(), updated_student.student_id)
            return True
        except Exception as e:
            print(f"Error updating student: {e}")
            return False
    
    def remove_student(self, student_id: str) -> bool:
        """Remove permanentemente um estudante da base de dados através do ID.

        Args:
            student_id (str): O ID do estudante que será excluído.

        Returns:
            bool: True se a exclusão foi executada com sucesso, False se houver falhas.
        """
        try:
            self._context.remove_entity(student_id)
            return True
        except Exception as e:
            print(f"Error removing student: {e}")
            return False
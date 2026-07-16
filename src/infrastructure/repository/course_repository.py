from typing import List

from src.domain.entities.course import Course
from src.domain.repository_contract.course_repository_contract import CourseRepositoryContract

from src.infrastructure.db_context.db_context import Context

class CourseRepository(CourseRepositoryContract):
    """Implementação concreta do repositório de cursos utilizando persistência em arquivos CSV.

    Esta classe implementa o contrato `CourseRepositoryContract` e faz a ponte entre 
    as operações do domínio de cursos e a camada física de armazenamento gerenciada pelo `Context`.

    Attributes:
        _context (Context): Instância do contexto de banco de dados/arquivo responsável pelas operações de I/O.
    """

    def __init__(self, context: Context):
        """Inicializa o repositório de cursos com o contexto de persistência fornecido.

        Args:
            context (Context): Instância ativa de Context configurada para persistência de cursos.
        """
        self._context = context
    
    def add_course(self, course: Course) -> bool:
        """Adiciona um novo curso ao arquivo de persistência.

        Serializa a entidade recebida no formato CSV e delega o salvamento para o contexto.

        Args:
            course (Course): Instância da entidade Course que será adicionada.

        Returns:
            bool: True se o curso foi salvo com sucesso, False caso ocorra alguma falha/exceção.
        """
        try:
            self._context.save_entity(course.to_csv())
            return True
        except Exception as e:
            print(f"Error adding course: {e}")
            return False

    def get_course_by_id(self, course_id: str) -> Course:
        """Busca um curso cadastrado através do seu identificador único.

        O método lê todas as entidades do arquivo físico de cursos e procura a linha 
        que se inicia com o ID do curso fornecido.

        Args:
            course_id (str): Identificador único do curso a ser recuperado.

        Returns:
            Course: Instância da entidade Course preenchida com os dados da linha CSV encontrada,
                    ou None se o curso não for localizado ou em caso de erro na operação.
        """
        try:
            file_reader = self._context.get_all_entities()
            for line in file_reader:
                if line.startswith(course_id):
                    return Course.from_csv(line)
            return None
        except Exception as e:
            print(f"Error retrieving course: {e}")
            return None

    def get_all_courses(self) -> List[Course]:
        """Recupera todos os cursos gravados no arquivo de persistência.

        Faz a leitura completa do arquivo de cursos e converte cada linha válida em 
        uma instância da entidade Course.

        Returns:
            List[Course]: Uma lista de objetos Course. Retorna uma lista vazia caso
                          não existam cursos registrados ou se ocorrer uma falha.
        """
        courses = []
        try:
            file_reader = self._context.get_all_entities()
            for line in file_reader:
                courses.append(Course.from_csv(line))
            return courses
        except Exception as e:
            print(f"Error retrieving all courses: {e}")
            return []

    def update_course(self, updated_course: Course) -> bool:
        """Atualiza os dados de um curso existente no arquivo de persistência.

        Serializa os novos dados da entidade e delega a modificação de linha baseada no ID ao contexto.

        Args:
            updated_course (Course): Entidade Course com os dados atualizados e contendo
                                     o ID do curso que sofrerá a substituição.

        Returns:
            bool: True se a atualização foi efetuada com sucesso, False caso ocorra alguma falha.
        """
        try:
            self._context.update_entity(updated_course.to_csv(), updated_course.course_id)
            return True
        except Exception as e:
            print(f"Error updating course: {e}")
            return False

    def remove_course(self, course_id: str) -> bool:
        """Remove o registro de um curso do arquivo de persistência com base no ID.

        Delega a exclusão física da linha contendo o ID correspondente ao contexto.

        Args:
            course_id (str): Identificador único do curso que será removido.

        Returns:
            bool: True se a remoção foi bem-sucedida, False se ocorrer uma falha no processo.
        """
        try:
            self._context.remove_entity(course_id)
            return True
        except Exception as e:
            print(f"Error removing course: {e}")
            return False
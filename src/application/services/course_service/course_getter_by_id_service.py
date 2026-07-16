from typing import Optional

from src.domain.entities.course import Course
from src.domain.repository_contract.course_repository_contract import CourseRepositoryContract
from src.application.services_contract.course_contract.course_getter_by_id_contract import CourseGetterByIdContract


class CourseGetterByIdService(CourseGetterByIdContract):
    """Serviço responsável por buscar os detalhes de um curso através do seu identificador.

    Esta classe implementa o contrato `CourseGetterByIdContract` e encapsula a lógica 
    para consultar um curso específico no repositório com base no ID fornecido pelo objeto.

    Attributes:
        _repository (CourseRepositoryContract): Repositório para consulta e persistência de cursos.
    """

    def __init__(self, course_repository: CourseRepositoryContract):
        """Inicializa o serviço de busca de cursos com o repositório necessário.

        Args:
            course_repository (CourseRepositoryContract): Instância do repositório de cursos.
        """
        self._repository = course_repository

    def get_course_by_id(self, course: Course) -> Optional[Course]:
        """Busca um curso no repositório utilizando o ID do curso informado.

        O método tenta localizar os dados atualizados do curso no banco de dados
        a partir da propriedade `course_id` da entidade passada como parâmetro.

        Args:
            course (Course): Uma instância da entidade Course contendo o `course_id` a ser buscado.

        Returns:
            Optional[Course]: A instância da entidade `Course` encontrada com os dados preenchidos 
                              ou `None` se o curso não for localizado ou se ocorrer uma falha na busca.
        """
        try:
            return self._repository.get_course_by_id(course.course_id)
        except Exception as e:
            print(f"Error occurred while fetching course by ID: {e}")
            return None
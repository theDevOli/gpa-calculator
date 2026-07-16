from typing import List

from src.domain.entities.course import Course
from src.domain.repository_contract.course_repository_contract import CourseRepositoryContract
from src.application.services_contract.course_contract.course_getter_contract import CourseGetterContract


class CourseGetterService(CourseGetterContract):
    """Serviço responsável por recuperar a listagem completa de cursos do sistema.

    Esta classe implementa o contrato `CourseGetterContract` e serve como ponto de entrada 
    para obter todos os registros de cursos armazenados, sem a aplicação de filtros.

    Attributes:
        _repository (CourseRepositoryContract): Repositório para consulta e persistência de cursos.
    """

    def __init__(self, course_repository: CourseRepositoryContract):
        """Inicializa o serviço de listagem de cursos com o repositório necessário.

        Args:
            course_repository (CourseRepositoryContract): Instância do repositório de cursos.
        """
        self._repository = course_repository

    def get_all_courses(self) -> List[Course]:
        """Recupera todos os cursos cadastrados no repositório.

        O método faz uma busca geral na base de dados de cursos. Se houver falha de 
        comunicação com a base ou qualquer outra exceção interna, o erro é capturado, 
        registrado no console, e uma lista vazia é retornada para manter a consistência da tipagem.

        Returns:
            List[Course]: Uma lista contendo todas as instâncias da entidade `Course` 
                          encontradas. Retorna uma lista vazia `[]` caso nenhum curso 
                          exista ou ocorra uma falha na operação.
        """
        try:
            return self._repository.get_all_courses()
        except Exception as e:
            print(f"Error occurred while fetching all courses: {e}")
            return []
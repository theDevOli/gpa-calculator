from src.domain.entities.course import Course
from src.domain.repository_contract.course_repository_contract import CourseRepositoryContract
from src.application.services_contract.course_contract.course_updatable_contract import CourseUpdatableContract


class CourseUpdatableService(CourseUpdatableContract):
    """Serviço responsável por atualizar as informações de um curso existente.

    Esta classe implementa o contrato `CourseUpdatableContract` e coordena as regras de negócio
    para atualizar os dados cadastrais de um curso, garantindo a sua existência prévia no repositório.

    Attributes:
        _repository (CourseRepositoryContract): Repositório para persistência, consulta e atualização de cursos.
    """

    def __init__(self, course_repository: CourseRepositoryContract):
        """Inicializa o serviço de atualização de cursos com o repositório necessário.

        Args:
            course_repository (CourseRepositoryContract): Instância do repositório de cursos.
        """
        self._repository = course_repository

    def update_course(self, to_update_course: Course) -> str:
        """Atualiza os dados de um curso existente no repositório.

        O método realiza as seguintes validações e etapas:
        1. Consulta o repositório utilizando o ID do curso fornecido para verificar se ele existe.
        2. Se encontrado, tenta aplicar as novas propriedades da entidade passada como parâmetro no banco.

        Args:
            to_update_course (Course): Instância da entidade Course contendo as novas informações
                                       e o `course_id` correspondente ao registro que será modificado.

        Returns:
            str: Uma mensagem descritiva indicando o sucesso ou o motivo da falha na operação.
                 Mensagens possíveis:
                 - "Curso atualizado com sucesso."
                 - "Curso nao encontrado."
                 - "Nao foi possivel atualizar o curso."
                 - "Erro ao atualizar curso" (em caso de exceções não tratadas).
        """
        try:
            existing_course = self._repository.get_course_by_id(to_update_course.course_id)

            if existing_course is None:
                return 'Curso nao encontrado.'
            
            was_updated = self._repository.update_course(to_update_course)
            if not was_updated:
                return 'Nao foi possivel atualizar o curso.'
            
            return "Curso atualizado com sucesso."
        except Exception as e:
            print(f"Error updating course: {e}")
            return "Erro ao atualizar curso"
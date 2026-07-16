from src.domain.entities.course import Course
from src.domain.repository_contract.course_repository_contract import CourseRepositoryContract
from src.domain.repository_contract.student_repository_contract import StudentRepositoryContract
from src.application.services_contract.course_contract.course_deletion_contract import CourseDeletionContract


class CourseDeletionService(CourseDeletionContract):
    """Serviço responsável por remover um curso e desvinculá-lo de um estudante.

    Esta classe implementa o contrato `CourseDeletionContract` e coordena a lógica de negócio
    necessária para deletar um curso do repositório de cursos e remover sua referência do 
    cadastro do estudante associado.

    Attributes:
        _course_repository (CourseRepositoryContract): Repositório para gerenciamento e persistência de cursos.
        _student_repository (StudentRepositoryContract): Repositório para gerenciamento e persistência de estudantes.
    """

    def __init__(self, course_repository: CourseRepositoryContract, student_repository: StudentRepositoryContract):
        """Inicializa o serviço de exclusão de cursos com os repositórios necessários.

        Args:
            course_repository (CourseRepositoryContract): Instância do repositório de cursos.
            student_repository (StudentRepositoryContract): Instância do repositório de estudantes.
        """
        self._course_repository = course_repository
        self._student_repository = student_repository

    def delete_course(self, student_id: str, course: Course) -> str:
        """Deleta um curso e remove sua associação do cadastro do estudante especificado.

        O método realiza as seguintes validações e etapas de negócio:
        1. Verifica se o estudante existe no banco de dados.
        2. Verifica se o curso informado existe no repositório.
        3. Remove o curso do repositório de cursos.
        4. Desvincula o ID do curso do cadastro do estudante e atualiza os dados do estudante.

        Args:
            student_id (str): Identificador único do estudante que possui o curso.
            course (Course): Instância da entidade Course que se deseja remover.

        Returns:
            str: Uma mensagem descritiva indicando o sucesso ou o motivo da falha na operação.
                 Mensagens possíveis:
                 - "Curso deletado com sucesso."
                 - "Nao foi possivel encontrar o estudante para deletar o curso."
                 - "Curso nao encontrado."
                 - "Nao foi possivel remover o curso."
                 - "Nao foi possivel atualizar o estudante."
                 - "Erro ao deletar curso" (em caso de exceções não tratadas durante o processo).
        """
        try:
            student_db = self._student_repository.get_student_by_id(student_id=str(student_id))
            if student_db is None: 
                return 'Nao foi possivel encontrar o estudante para deletar o curso.'

            course_db = self._course_repository.get_course_by_id(course.course_id)
            if course_db is None:
                return 'Curso nao encontrado.'

            was_removed = self._course_repository.remove_course(course.course_id)
            if not was_removed:
                return 'Nao foi possivel remover o curso.'

            student_db.remove_course(course_id=course.course_id)
            is_updated = self._student_repository.update_student(student_db)
            if not is_updated: 
                return 'Nao foi possivel atualizar o estudante.'
            
            return 'Curso deletado com sucesso.'
        except Exception as e:
            print(f"Error deleting course: {e}")
            return "Erro ao deletar curso"
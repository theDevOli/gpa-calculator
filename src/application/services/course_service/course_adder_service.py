from src.domain.entities.course import Course
from src.domain.repository_contract.course_repository_contract import CourseRepositoryContract
from src.domain.repository_contract.student_repository_contract import StudentRepositoryContract
from src.application.services_contract.course_contract.course_adder_contract import CourseAdderContract

class CourseAdderService(CourseAdderContract):
    """Serviço responsável por associar um novo curso a um estudante.

    Esta classe implementa o contrato `CourseAdderContract` e coordena a lógica de negócio
    necessária para validar a existência do estudante, verificar se o curso já está associado
    a ele, persistir o novo curso no repositório e atualizar o cadastro do estudante.

    Attributes:
        _course_repository (CourseRepositoryContract): Repositório para persistência e consulta de cursos.
        _student_repository (StudentRepositoryContract): Repositório para persistência e consulta de estudantes.
    """

    def __init__(self, course_repository: CourseRepositoryContract, student_repository: StudentRepositoryContract):
        """Inicializa o serviço de adição de cursos com os repositórios necessários.

        Args:
            course_repository (CourseRepositoryContract): Instância do repositório de cursos.
            student_repository (StudentRepositoryContract): Instância do repositório de estudantes.
        """
        self._course_repository = course_repository
        self._student_repository = student_repository

    def add_course(self, student_id: str, new_course: Course) -> str:
        """Adiciona um novo curso e o vincula ao estudante especificado.

        O método realiza as seguintes validações e etapas:
        1. Verifica se o estudante existe no banco de dados.
        2. Certifica-se de que o estudante já não possui um curso cadastrado com o mesmo nome.
        3. Adiciona o novo curso ao repositório de cursos.
        4. Vincula o ID do curso criado ao cadastro do estudante e atualiza o estudante no banco.

        Args:
            student_id (str): Identificador único do estudante.
            new_course (Course): Instância da entidade Course que se deseja adicionar.

        Returns:
            str: Uma mensagem descritiva indicando o sucesso ou o motivo da falha na operação.
                 Mensagens possíveis:
                 - "Curso adicionado com sucesso."
                 - "Nao foi possivel encontrar o estudante para adicionar o curso."
                 - "Curso já existe para este estudante."
                 - "Nao foi possivel adicionar o curso."
                 - "Nao foi possivel atualizar o estudante."
                 - "Erro ao adicionar curso" (em caso de exceções não tratadas).
        """
        try:
            student_db = self._student_repository.get_student_by_id(student_id=str(student_id))
            if student_db == None: 
                return 'Nao foi possivel encontrar o estudante para adicionar o curso.'

            found_course = list(filter(lambda course_id: self._course_repository.get_course_by_id(course_id).name == new_course.name, student_db.courses))
            if len(found_course) > 0: 
                return 'Curso já existe para este estudante.'
            
            wasAdded = self._course_repository.add_course(new_course)
            if not wasAdded: 
                return 'Nao foi possivel adicionar o curso.'

            student_db.add_course(new_course.course_id)
            wasUpdated = self._student_repository.update_student(student_db)
            if not wasUpdated: 
                return 'Nao foi possivel atualizar o estudante.'

            return "Curso adicionado com sucesso."
        except Exception as e:
            print(f"Error adding course: {e}")
            return "Erro ao adicionar curso"
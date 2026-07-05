import pytest
from unittest.mock import MagicMock

from src import Course, CourseAdderService, CourseGetterByIdService, CourseGetterService, CourseDeletionService, CourseUpdatableService

@pytest.fixture
def course():
    """Fixture que fornece um objeto Course padrão para os testes do serviço."""
    # Certifique-se de que os parâmetros batem com o construtor da sua entidade Course
    return Course(name="Arquitetura de Software", credit_hours=4, grade=10.0)

def test_add_course_success(course):
    """Garante que o curso é adicionado com sucesso se não houver outro com o mesmo nome."""
    # Arrange
    mock_repository = MagicMock()
    # O repositório retorna uma lista vazia ou com cursos de nomes diferentes
    mock_repository.get_all_courses.return_value = []
    mock_repository.add_course.return_value = True
    
    service = CourseAdderService(course_repository=mock_repository)

    # Act
    result = service.add_course(course)

    # Assert
    assert result is True
    mock_repository.get_all_courses.assert_called_once()
    mock_repository.add_course.assert_called_once_with(course)


def test_add_course_fails_when_name_already_exists(course):
    """Garante que o serviço retorna False e barra a inserção se o nome do curso já existir."""
    # Arrange
    mock_repository = MagicMock()
    # Cria um curso com o mesmo nome para simular a duplicidade no banco/arquivo
    existing_course = Course(name="Arquitetura de Software", credit_hours=4, grade=0.0)
    mock_repository.get_all_courses.return_value = [existing_course]
    
    service = CourseAdderService(course_repository=mock_repository)

    # Act
    result = service.add_course(course)

    # Assert
    assert result is False
    mock_repository.get_all_courses.assert_called_once()
    # Garante de forma estrita que o repositório NUNCA foi acionado para salvar o duplicado
    mock_repository.add_course.assert_not_called()

def test_add_course_exception_handling(course):
    """Garante que falhas catastróficas ou erros no repositório são tratados e retornam False."""
    # Arrange
    mock_repository = MagicMock()
    # Força uma exceção inesperada logo na listagem inicial de validação
    mock_repository.get_all_courses.side_effect = Exception("File permission error")
    
    service = CourseAdderService(course_repository=mock_repository)

    # Act
    result = service.add_course(course)

    # Assert
    assert result is False
    mock_repository.add_course.assert_not_called()

def test_get_course_by_id_success(course):
    """Garante que o serviço retorna o objeto Course correto quando o ID existe no repositório."""
    # Arrange
    mock_repository = MagicMock()
    # O repositório finge encontrar o curso correspondente ao ID informado
    mock_repository.get_course_by_id.return_value = course
    
    service = CourseGetterByIdService(course_repository=mock_repository)

    # Act
    result = service.get_course_by_id(course)

    # Assert
    assert result is not None
    assert result.course_id == course.course_id
    assert result.name == "Arquitetura de Software"
    mock_repository.get_course_by_id.assert_called_once_with(course.course_id)


def test_get_course_by_id_not_found():
    """Garante que o serviço retorna None caso o ID fornecido não seja localizado."""
    # Arrange
    mock_repository = MagicMock()
    # O repositório simula que o ID procurado não existe no arquivo/banco
    mock_repository.get_course_by_id.return_value = None
    test_course = Course(name="Curso Inexistente", credit_hours=0, grade=0.0)
    
    service = CourseGetterByIdService(course_repository=mock_repository)
    target_id = test_course.course_id

    # Act
    result = service.get_course_by_id(test_course)

    # Assert
    assert result is None
    mock_repository.get_course_by_id.assert_called_once_with(target_id)


def test_get_course_by_id_exception_handling():
    """Garante que falhas catastróficas na infraestrutura são tratadas e o serviço retorna None."""
    # Arrange
    mock_repository = MagicMock()
    # Força uma exceção no repositório simulando falha física de I/O ou arquivo ausente
    mock_repository.get_course_by_id.side_effect = Exception("File system error")
    
    service = CourseGetterByIdService(course_repository=mock_repository)
    test_course = Course(name="Curso Inexistente", credit_hours=0, grade=0.0)
    target_id = test_course.course_id

    # Act
    result = service.get_course_by_id(test_course)

    # Assert
    assert result is None
    mock_repository.get_course_by_id.assert_called_once_with(target_id)

def test_get_all_courses_success(course):
    """Garante que o serviço retorna a lista completa de cursos vinda do repositório."""
    # Arrange
    mock_repository = MagicMock()
    c1 = course
    c2 = Course(name="Estrutura de Dados", credit_hours=2, grade=8.5)
    
    # Configura o mock para retornar a lista de cursos simulada
    mock_repository.get_all_courses.return_value = [c1, c2]
    
    service = CourseGetterService(course_repository=mock_repository)

    # Act
    result = service.get_all_courses()

    # Assert
    assert len(result) == 2
    assert result[0].name == "Arquitetura de Software"
    assert result[1].name == "Estrutura de Dados"
    mock_repository.get_all_courses.assert_called_once()


def test_get_all_courses_returns_empty_list_when_none_exists():
    """Garante que o serviço retorna uma lista vazia se não houver registros no repositório."""
    # Arrange
    mock_repository = MagicMock()
    mock_repository.get_all_courses.return_value = []
    
    service = CourseGetterService(course_repository=mock_repository)

    # Act
    result = service.get_all_courses()

    # Assert
    assert result == []
    mock_repository.get_all_courses.assert_called_once()


def test_get_all_courses_exception_handling():
    """Garante que falhas catastróficas na camada de infraestrutura retornam uma lista vazia de forma segura."""
    # Arrange
    mock_repository = MagicMock()
    # Força uma exceção simulando erro de leitura ou arquivo corrompido
    mock_repository.get_all_courses.side_effect = Exception("Database unreadable")
    
    service = CourseGetterService(course_repository=mock_repository)

    # Act
    result = service.get_all_courses()

    # Assert
    assert result == []
    mock_repository.get_all_courses.assert_called_once()

def test_delete_course_success(course):
    """Garante que o curso é deletado com sucesso se for localizado pelo nome."""
    # Arrange
    mock_repository = MagicMock()
    # O repositório retorna uma lista contendo o curso que desejamos apagar
    mock_repository.get_all_courses.return_value = [course]
    mock_repository.remove_course.return_value = True
    
    service = CourseDeletionService(course_repository=mock_repository)

    # Act
    result = service.delete_course(course)

    # Assert
    assert result is True
    mock_repository.get_all_courses.assert_called_once()
    mock_repository.remove_course.assert_called_once_with(course.course_id)


def test_delete_course_fails_if_not_found(course):
    """Garante que retorna False e não tenta remover se o curso não existir na listagem."""
    # Arrange
    mock_repository = MagicMock()
    # O repositório retorna uma lista vazia ou com cursos de nomes diferentes
    mock_repository.get_all_courses.return_value = []
    
    service = CourseDeletionService(course_repository=mock_repository)

    # Act
    result = service.delete_course(course)

    # Assert
    assert result is False
    mock_repository.get_all_courses.assert_called_once()
    # Garante que o repositório nunca tentou efetuar a remoção física
    mock_repository.remove_course.assert_not_called()


def test_delete_course_exception_handling(course):
    """Garante que falhas internas ou de I/O no repositório são tratadas e retornam False."""
    # Arrange
    mock_repository = MagicMock()
    # Força uma exceção inesperada logo na consulta inicial do serviço
    mock_repository.get_all_courses.side_effect = Exception("Disk failure")
    
    service = CourseDeletionService(course_repository=mock_repository)

    # Act
    result = service.delete_course(course)

    # Assert
    assert result is False
    mock_repository.remove_course.assert_not_called()

def test_update_course_success(course):
    """Garante que o curso é atualizado com sucesso se ele for localizado pelo nome."""
    # Arrange
    mock_repository = MagicMock()
    # O repositório simula que o curso antigo existe na base de dados
    mock_repository.get_all_courses.return_value = [course]
    mock_repository.update.return_value = True
    
    service = CourseUpdatableService(course_repository=mock_repository)

    # Act
    result = service.update_course(course)

    # Assert
    assert result is True
    mock_repository.get_all_courses.assert_called_once()
    mock_repository.update.assert_called_once_with(course)


def test_update_course_fails_if_not_found(course):
    """Garante que o serviço retorna False e cancela a operação se o curso não existir."""
    # Arrange
    mock_repository = MagicMock()
    # O repositório simula que não há nenhum curso com esse nome cadastrado
    mock_repository.get_all_courses.return_value = []
    
    service = CourseUpdatableService(course_repository=mock_repository)

    # Act
    result = service.update_course(course)

    # Assert
    assert result is False
    mock_repository.get_all_courses.assert_called_once()
    # Garante de forma estrita que o método físico de persistência nunca foi chamado
    mock_repository.update.assert_not_called()


def test_update_course_exception_handling(course):
    """Garante que exceções internas ou travamentos de arquivo retornam False com segurança."""
    # Arrange
    mock_repository = MagicMock()
    # Força uma exceção catastrófica na primeira chamada do método
    mock_repository.get_all_courses.side_effect = Exception("Database file is locked")
    
    service = CourseUpdatableService(course_repository=mock_repository)

    # Act
    result = service.update_course(course)

    # Assert
    assert result is False
    mock_repository.update.assert_not_called()
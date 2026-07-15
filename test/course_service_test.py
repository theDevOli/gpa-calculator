"""Módulo de testes unitários para a camada de serviços de cursos (Course Services).

Este módulo valida os fluxos de negócios (casos de uso) para manipulação,
criação, leitura, atualização e remoção de cursos utilizando dublês de teste (Mocks)
para as dependências de repositório e contexto.
"""

import pytest
from unittest.mock import MagicMock

from src import (
    Course,
    CourseAdderService,
    CourseGetterByIdService,
    CourseGetterService,
    CourseDeletionService,
    CourseUpdatableService,
)


@pytest.fixture
def course() -> Course:
    """Fixture que fornece um objeto Course padrão para os testes do serviço.

    Returns:
        Course: Uma instância padrão configurada para uso nos testes de serviço.
    """
    return Course(name="Arquitetura de Software", credit_hours=4, grade=10.0)


# ==============================================================================
# TESTES: ADIÇÃO DE CURSOS (CourseAdderService)
# ==============================================================================

def test_add_course_success() -> None:
    """Garante que o curso é adicionado com sucesso se não houver duplicidade de nome.

    Valida o fluxo feliz em que o estudante existe, não possui nenhum curso com o
    mesmo nome cadastrado e o repositório salva as alterações corretamente.
    """
    # Arrange
    course_mock_repository = MagicMock()
    student_mock_repository = MagicMock()

    # Configura o mock do estudante (ele começa sem nenhum curso)
    student_mock = MagicMock()
    student_mock.courses = []
    student_mock_repository.get_student_by_id.return_value = student_mock

    # Simula que não há cursos duplicados (retorna lista vazia ao buscar os cursos do estudante)
    course_mock_repository.get_courses_by_ids.return_value = []
    
    # O repositório de cursos retorna True indicando que salvou com sucesso
    course_mock_repository.add_course.return_value = True
    # O repositório de estudantes retorna True indicando que atualizou com sucesso
    student_mock_repository.update_student.return_value = True
    
    service = CourseAdderService(course_repository=course_mock_repository, student_repository=student_mock_repository)
    new_course = Course(name="Arquitetura de Software", credit_hours=4, grade=0.0)
    new_course.course_id = "course_123"

    # Act - Passando os dois parâmetros necessários
    result = service.add_course(student_id="student_789", new_course=new_course)

    # Assert
    assert result == "Curso adicionado com sucesso."
    student_mock_repository.get_student_by_id.assert_called_once_with(student_id="student_789")
    course_mock_repository.add_course.assert_called_once_with(new_course)
    student_mock.add_course.assert_called_once_with("course_123")
    student_mock_repository.update_student.assert_called_once_with(student_mock)


def test_add_course_fails_when_name_already_exists() -> None:
    """Garante que o serviço barra a inserção se o nome do curso já existir.

    Valida o comportamento de restrição de unicidade por nome de curso para o 
    mesmo estudante.
    """
    # Arrange
    course_mock_repository = MagicMock()
    student_mock_repository = MagicMock()

    # O estudante já possui o curso ID "course_123" vinculado
    student_mock = MagicMock()
    student_mock.courses = ["course_123"]
    student_mock_repository.get_student_by_id.return_value = student_mock

    # O repositório vai retornar um curso com o mesmo nome do que estamos tentando criar
    existing_course = Course(name="Arquitetura de Software", credit_hours=4, grade=0.0)
    existing_course.course_id = "course_123"
    course_mock_repository.get_courses_by_ids.return_value = [existing_course]

    service = CourseAdderService(course_repository=course_mock_repository, student_repository=student_mock_repository)
    new_course = Course(name="Arquitetura de Software", credit_hours=4, grade=0.0)

    # Act
    result = service.add_course(student_id="student_789", new_course=new_course)

    # Assert
    assert result == "Curso já existe para este estudante."
    course_mock_repository.add_course.assert_not_called()
    student_mock_repository.update_student.assert_not_called()


def test_add_course_exception_handling() -> None:
    """Garante que falhas no repositório são tratadas e retornam a string de erro.

    Simula uma exceção catastrófica de persistência de dados durante a tentativa de busca.
    """
    # Arrange
    course_mock_repository = MagicMock()
    student_mock_repository = MagicMock()
    
    # Força uma exceção inesperada logo na busca do estudante
    student_mock_repository.get_student_by_id.side_effect = Exception("File permission error ou Database Down")
    
    service = CourseAdderService(course_repository=course_mock_repository, student_repository=student_mock_repository)
    new_course = Course(name="Arquitetura de Software", credit_hours=4, grade=0.0)

    # Act
    result = service.add_course(student_id="student_789", new_course=new_course)

    # Assert
    assert result == "Erro ao adicionar curso"
    course_mock_repository.add_course.assert_not_called()


# ==============================================================================
# TESTES: CONSULTA DE CURSO POR ID (CourseGetterByIdService)
# ==============================================================================

def test_get_course_by_id_success(course: Course) -> None:
    """Garante que o serviço retorna o objeto Course correto quando o ID existe.

    Verifica se a requisição é corretamente encaminhada ao repositório e o objeto é retornado.
    """
    # Arrange
    course_mock_repository = MagicMock()
    # O repositório finge encontrar o curso correspondente ao ID informado
    course_mock_repository.get_course_by_id.return_value = course
    
    service = CourseGetterByIdService(course_repository=course_mock_repository)

    # Act
    result = service.get_course_by_id(course)

    # Assert
    assert result is not None
    assert result.course_id == course.course_id
    assert result.name == "Arquitetura de Software"
    course_mock_repository.get_course_by_id.assert_called_once_with(course.course_id)


def test_get_course_by_id_not_found() -> None:
    """Garante que o serviço retorna None caso o ID fornecido não seja localizado.

    Valida o comportamento seguro quando o repositório devolve None para o identificador.
    """
    # Arrange
    course_mock_repository = MagicMock()
    # O repositório simula que o ID procurado não existe no arquivo/banco
    course_mock_repository.get_course_by_id.return_value = None
    test_course = Course(name="Curso Inexistente", credit_hours=0, grade=0.0)
    
    service = CourseGetterByIdService(course_repository=course_mock_repository)
    target_id = test_course.course_id

    # Act
    result = service.get_course_by_id(test_course)

    # Assert
    assert result is None
    course_mock_repository.get_course_by_id.assert_called_once_with(target_id)


def test_get_course_by_id_exception_handling() -> None:
    """Garante que falhas catastróficas na infraestrutura retornam None graciosamente.

    Trata exceções lançadas pelo driver de banco ou manipulação de arquivos físicos.
    """
    # Arrange
    course_mock_repository = MagicMock()
    # Força uma exceção no repositório simulando falha física de I/O ou arquivo ausente
    course_mock_repository.get_course_by_id.side_effect = Exception("File system error")
    
    service = CourseGetterByIdService(course_repository=course_mock_repository)
    test_course = Course(name="Curso Inexistente", credit_hours=0, grade=0.0)
    target_id = test_course.course_id

    # Act
    result = service.get_course_by_id(test_course)

    # Assert
    assert result is None
    course_mock_repository.get_course_by_id.assert_called_once_with(target_id)


# ==============================================================================
# TESTES: CONSULTA DE TODOS OS CURSOS (CourseGetterService)
# ==============================================================================

def test_get_all_courses_success(course: Course) -> None:
    """Garante que o serviço retorna a lista completa de cursos cadastrados.

    Verifica o retorno de todos os objetos mapeados no repositório.
    """
    # Arrange
    course_mock_repository = MagicMock()
    c1 = course
    c2 = Course(name="Estrutura de Dados", credit_hours=2, grade=8.5)
    
    # Configura o mock para retornar a lista de cursos simulada
    course_mock_repository.get_all_courses.return_value = [c1, c2]
    
    service = CourseGetterService(course_repository=course_mock_repository)

    # Act
    result = service.get_all_courses()

    # Assert
    assert len(result) == 2
    assert result[0].name == "Arquitetura de Software"
    assert result[1].name == "Estrutura de Dados"
    course_mock_repository.get_all_courses.assert_called_once()


def test_get_all_courses_returns_empty_list_when_none_exists() -> None:
    """Garante que o serviço retorna uma lista vazia se não houver registros.

    Valida o comportamento seguro sem lançar exceções para base de dados vazia.
    """
    # Arrange
    course_mock_repository = MagicMock()
    course_mock_repository.get_all_courses.return_value = []
    
    service = CourseGetterService(course_repository=course_mock_repository)

    # Act
    result = service.get_all_courses()

    # Assert
    assert result == []
    course_mock_repository.get_all_courses.assert_called_once()


def test_get_all_courses_exception_handling() -> None:
    """Garante que falhas de infraestrutura são tratadas retornando lista vazia.

    Assegura que o sistema não quebra na UI caso o banco esteja indisponível.
    """
    # Arrange
    course_mock_repository = MagicMock()
    # Força uma exceção simulando erro de leitura ou arquivo corrompido
    course_mock_repository.get_all_courses.side_effect = Exception("Database unreadable")
    
    service = CourseGetterService(course_repository=course_mock_repository)

    # Act
    result = service.get_all_courses()

    # Assert
    assert result == []
    course_mock_repository.get_all_courses.assert_called_once()


# ==============================================================================
# TESTES: EXCLUSÃO DE CURSOS (CourseDeletionService)
# ==============================================================================

def test_delete_course_success() -> None:
    """Garante que o curso é deletado e desvinculado do estudante com sucesso.

    Valida o sincronismo entre a remoção do curso na entidade Course e a 
    desassociação no agregado de Student.
    """
    # Arrange
    course_mock_repository = MagicMock()
    student_mock_repository = MagicMock()

    # Cria o curso que queremos deletar
    course = Course(name="Arquitetura de Software", credit_hours=4, grade=0.0)
    course.course_id = "course_123"

    # Mock do estudante que possui esse curso
    student_mock = MagicMock()
    student_mock_repository.get_student_by_id.return_value = student_mock

    # O repositório encontra o curso e as operações retornam sucesso (True)
    course_mock_repository.get_course_by_id.return_value = course
    course_mock_repository.remove_course.return_value = True
    student_mock_repository.update_student.return_value = True
    
    service = CourseDeletionService(course_repository=course_mock_repository, student_repository=student_mock_repository)

    # Act
    result = service.delete_course(student_id="student_789", course=course)

    # Assert
    assert result == 'Curso deletado com sucesso.'
    student_mock_repository.get_student_by_id.assert_called_once_with(student_id="student_789")
    course_mock_repository.get_course_by_id.assert_called_once_with("course_123")
    course_mock_repository.remove_course.assert_called_once_with("course_123")
    student_mock.remove_course.assert_called_once_with(course_id="course_123")
    student_mock_repository.update_student.assert_called_once_with(student_mock)


def test_delete_course_fails_if_not_found() -> None:
    """Garante que retorna uma mensagem clara caso o curso não exista.

    Verifica o comportamento protetor para impedir alterações se o ID do curso 
    for inexistente ou inválido.
    """
    # Arrange
    course_mock_repository = MagicMock()
    student_mock_repository = MagicMock()

    # O estudante existe
    student_mock = MagicMock()
    student_mock_repository.get_student_by_id.return_value = student_mock

    # O curso NÃO é encontrado no banco de dados (retorna None)
    course_mock_repository.get_course_by_id.return_value = None
    
    service = CourseDeletionService(course_repository=course_mock_repository, student_repository=student_mock_repository)
    course = Course(name="Curso Fantasma", credit_hours=2, grade=0.0)
    course.course_id = "phantom_999"

    # Act
    result = service.delete_course(student_id="student_789", course=course)

    # Assert
    assert result == 'Curso nao encontrado.'
    course_mock_repository.get_course_by_id.assert_called_once_with("phantom_999")
    # Garante que o fluxo travou e não alterou nada
    course_mock_repository.remove_course.assert_not_called()
    student_mock.remove_course.assert_not_called()


def test_delete_course_exception_handling() -> None:
    """Garante que exceções de I/O são tratadas de forma segura com retorno genérico.

    Verifica o tratamento contra falhas graves na persistência ao tentar excluir registros.
    """
    # Arrange
    course_mock_repository = MagicMock()
    student_mock_repository = MagicMock()
    
    # Força uma exceção inesperada logo na primeira consulta (busca do estudante)
    student_mock_repository.get_student_by_id.side_effect = Exception("Disk failure")
    
    service = CourseDeletionService(course_repository=course_mock_repository, student_repository=student_mock_repository)
    course = Course(name="Arquitetura de Software", credit_hours=4, grade=0.0)

    # Act
    result = service.delete_course(student_id="student_789", course=course)

    # Assert
    assert result == "Erro ao deletar curso"
    course_mock_repository.remove_course.assert_not_called()


# ==============================================================================
# TESTES: ATUALIZAÇÃO DE CURSOS (CourseUpdatableService)
# ==============================================================================

def test_update_course_success() -> None:
    """Garante que o curso é atualizado corretamente caso ele exista.

    Assegura que as alterações de campos permitidos são salvas na persistência.
    """
    # Arrange
    course_mock_repository = MagicMock()
    
    course_to_update = Course(name="Arquitetura Avançada", credit_hours=5, grade=10.0)
    course_to_update.course_id = "course_123"

    # O repositório confirma que o curso antigo existe e que a atualização deu certo
    course_mock_repository.get_course_by_id.return_value = course_to_update
    course_mock_repository.update_course.return_value = True
    
    service = CourseUpdatableService(course_repository=course_mock_repository)

    # Act
    result = service.update_course(course_to_update)

    # Assert
    assert result == "Curso atualizado com sucesso."
    course_mock_repository.get_course_by_id.assert_called_once_with("course_123")
    course_mock_repository.update_course.assert_called_once_with(course_to_update)


def test_update_course_fails_if_not_found() -> None:
    """Garante que o serviço impede a atualização se o curso não for localizado.

    Valida que o repositório não é chamado desnecessariamente se a entidade 
    original não existe.
    """
    # Arrange
    course_mock_repository = MagicMock()
    # Simula que o curso não foi encontrado por ID
    course_mock_repository.get_course_by_id.return_value = None
    
    service = CourseUpdatableService(course_repository=course_mock_repository)
    course_to_update = Course(name="Curso Inexistente", credit_hours=2, grade=0.0)
    course_to_update.course_id = "ghost_id"

    # Act
    result = service.update_course(course_to_update)

    # Assert
    assert result == 'Curso nao encontrado.'
    course_mock_repository.get_course_by_id.assert_called_once_with("ghost_id")
    course_mock_repository.update_course.assert_not_called()


def test_update_course_exception_handling() -> None:
    """Garante que falhas internas ou timeouts disparam a mensagem de erro genérica.

    Verifica se erros internos de banco no update são capturados e mapeados de 
    forma limpa.
    """
    # Arrange
    course_mock_repository = MagicMock()
    course_mock_repository.get_course_by_id.side_effect = Exception("Database timeout")
    
    service = CourseUpdatableService(course_repository=course_mock_repository)
    course_to_update = Course(name="Arquitetura", credit_hours=4, grade=0.0)

    # Act
    result = service.update_course(course_to_update)

    # Assert
    assert result == "Erro ao atualizar curso"
    course_mock_repository.update_course.assert_not_called()

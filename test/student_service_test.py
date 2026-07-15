"""Módulo de testes unitários para os serviços de estudante (Student Services).

Este módulo valida as regras de negócio para a criação, consulta, remoção e 
atualização de estudantes. Ele faz uso de fixtures do pytest e dublês de teste 
(mocks) para simular o comportamento dos repositórios envolvidos nas operações.
"""

import pytest
from unittest.mock import MagicMock

from src import (
    Student,
    StudentAdderService,
    StudentGetterByIdService,
    StudentGetterService,
    StudentDeletionService,
    StudentUpdatableService,
)


@pytest.fixture
def student() -> Student:
    """Fixture que fornece um objeto Student padrão para os testes do serviço.

    Returns:
        Student: Uma instância de estudante configurada com dados válidos de teste.
    """
    return Student(name="Daniel", student_tax_id="123.456.789-00")


# ==============================================================================
# TESTES: ADIÇÃO DE ESTUDANTES (StudentAdderService)
# ==============================================================================

def test_add_student_success(student: Student) -> None:
    """Garante que o estudante é adicionado com sucesso se o CPF não existir.

    Valida o fluxo feliz em que o CPF não é duplicado e a operação de escrita 
    na camada de persistência retorna verdadeiro.
    """
    # Arrange
    repository_mock = MagicMock()
    repository_mock.get_student_by_tax_id.return_value = None
    repository_mock.add_student.return_value = True

    service = StudentAdderService(student_repository=repository_mock)

    # Act
    result = service.add_student(student)

    # Assert
    assert result == 'Sucesso ao adicionar estudante.'
    repository_mock.get_student_by_tax_id.assert_called_once_with(student.student_tax_id)
    repository_mock.add_student.assert_called_once_with(student)


def test_add_student_fails_when_student_already_exists(student: Student) -> None:
    """Garante que o serviço barra a inserção se o CPF já estiver cadastrado.

    Valida se a regra de unicidade pelo CPF (tax_id) impede chamadas de persistência 
    desnecessárias no banco de dados.
    """
    # Arrange
    repository_mock = MagicMock()
    repository_mock.get_student_by_tax_id.return_value = student

    service = StudentAdderService(student_repository=repository_mock)

    # Act
    result = service.add_student(student)

    # Assert
    assert result == 'Estudante já existe.'
    repository_mock.get_student_by_tax_id.assert_called_once_with(student.student_tax_id)
    repository_mock.add_student.assert_not_called()


def test_add_student_fails_when_repository_cannot_save(student: Student) -> None:
    """Garante o retorno correto se o repositório falhar no salvamento físico.

    Valida a resposta do serviço quando, apesar de passar pelas validações de negócio, 
    o repositório falha ao persistir os dados e retorna falso.
    """
    # Arrange
    repository_mock = MagicMock()
    repository_mock.get_student_by_tax_id.return_value = None
    repository_mock.add_student.return_value = False

    service = StudentAdderService(student_repository=repository_mock)

    # Act
    result = service.add_student(student)

    # Assert
    assert result == 'Nao foi possivel adicionar o estudante.'
    repository_mock.get_student_by_tax_id.assert_called_once_with(student.student_tax_id)
    repository_mock.add_student.assert_called_once_with(student)


def test_add_student_exception_handling(student: Student) -> None:
    """Garante que exceções inesperadas na infraestrutura são devidamente tratadas.

    Assegura que erros catastróficos de conexão ou banco de dados indisponível 
    são capturados sem quebrar o fluxo da aplicação.
    """
    # Arrange
    repository_mock = MagicMock()
    repository_mock.get_student_by_tax_id.side_effect = Exception("Database connection timeout")

    service = StudentAdderService(student_repository=repository_mock)

    # Act
    result = service.add_student(student)

    # Assert
    assert result == "Erro ao adicionar estudante"
    repository_mock.add_student.assert_not_called()


# ==============================================================================
# TESTES: CONSULTA DE ESTUDANTE POR ID (StudentGetterByIdService)
# ==============================================================================

def test_student_getter_by_id_success(student: Student) -> None:
    """Garante que o serviço retorna o objeto Student correto quando o ID existe.

    Verifica o carregamento bem-sucedido dos dados do estudante e sua correta 
    integração com o repositório de cursos.
    """
    # Arrange
    student_mock_repository = MagicMock()
    course_mock_repository = MagicMock()

    student_mock_repository.get_student_by_id.return_value = student
    course_mock_repository.get_all_courses.return_value = []
    
    service = StudentGetterByIdService(
        student_repository=student_mock_repository, 
        course_repository=course_mock_repository
    )

    # Act
    result = service.get_student_by_id(student)

    # Assert
    assert result is not None
    assert result.student_id == student.student_id
    assert result.name == student.name
    student_mock_repository.get_student_by_id.assert_called_once_with(student_id=student.student_id)
    course_mock_repository.get_all_courses.assert_called_once()


def test_student_getter_by_id_not_found() -> None:
    """Garante que o serviço retorna None se o ID não existir no repositório.

    Assegura que o fluxo de cursos associados não seja disparado caso a busca do 
    estudante pelo ID original falhe.
    """
    # Arrange
    student_mock_repository = MagicMock()
    course_mock_repository = MagicMock()

    student_mock_repository.get_student_by_id.return_value = None
    test_student = Student(name="Fake", student_tax_id="000.000.000-00")
    
    service = StudentGetterByIdService(
        student_repository=student_mock_repository, 
        course_repository=course_mock_repository
    )

    # Act
    result = service.get_student_by_id(student=test_student)

    # Assert
    assert result is None
    student_mock_repository.get_student_by_id.assert_called_once_with(student_id=test_student.student_id)
    course_mock_repository.get_all_courses.assert_not_called()


def test_student_getter_by_id_exception_handling() -> None:
    """Garante que o serviço captura exceções do repositório de forma segura.

    Valida se falhas graves de leitura ou I/O retornam graciosamente um valor nulo.
    """
    # Arrange
    student_mock_repository = MagicMock()
    course_mock_repository = MagicMock()

    student_mock_repository.get_student_by_id.side_effect = Exception("File read error")
    
    service = StudentGetterByIdService(
        student_repository=student_mock_repository, 
        course_repository=course_mock_repository
    )

    # Act
    result = service.get_student_by_id("qualquer-id")

    # Assert
    assert result is None


# ==============================================================================
# TESTES: CONSULTA DE TODOS OS ESTUDANTES (StudentGetterService)
# ==============================================================================

def test_student_getter_success(student: Student) -> None:
    """Garante que o serviço retorna a lista completa de estudantes.

    Valida o mapeamento e retorno correto de múltiplos registros recuperados da 
    camada de repositório.
    """
    # Arrange
    student_mock_repository = MagicMock()
    course_mock_repository = MagicMock()
    s1 = student
    s2 = Student(name="Maria", student_tax_id="987.654.321-11")
    
    student_mock_repository.get_all_students.return_value = [s1, s2]

    service = StudentGetterService(
        student_repository=student_mock_repository, 
        course_repository=course_mock_repository
    )

    # Act
    result = service.get_all_students()

    # Assert
    assert len(result) == 2
    assert result[0].name == "Daniel"
    assert result[1].name == "Maria"
    student_mock_repository.get_all_students.assert_called_once()


def test_student_getter_returns_empty_list_when_no_students() -> None:
    """Garante que o serviço retorna uma lista vazia se não houver registros.

    Valida se o fluxo é concluído com sucesso e sem erros na ausência de estudantes.
    """
    # Arrange
    student_mock_repository = MagicMock()
    course_mock_repository = MagicMock()
    student_mock_repository.get_all_students.return_value = []
    
    service = StudentGetterService(
        student_repository=student_mock_repository, 
        course_repository=course_mock_repository
    )

    # Act
    result = service.get_all_students()

    # Assert
    assert result == []
    student_mock_repository.get_all_students.assert_called_once()


def test_student_getter_exception_handling() -> None:
    """Garante que o serviço trata falhas do repositório retornando lista vazia.

    Evita falhas de tela na interface gráfica retornando uma lista vazia segura no 
    caso de indisponibilidade física dos arquivos de armazenamento.
    """
    # Arrange
    student_mock_repository = MagicMock()
    course_mock_repository = MagicMock()
    student_mock_repository.get_all_students.side_effect = Exception("IO Error")
    
    service = StudentGetterService(
        student_repository=student_mock_repository, 
        course_repository=course_mock_repository
    )

    # Act
    result = service.get_all_students()

    # Assert
    assert result == []


# ==============================================================================
# TESTES: EXCLUSÃO DE ESTUDANTES (StudentDeletionService)
# ==============================================================================

def test_delete_student_success(student: Student) -> None:
    """Garante que o estudante é removido com sucesso se existir na base.

    Valida se as consultas por ID e chamadas de remoção físicas são devidamente 
    disparadas e respondidas com a mensagem de sucesso padrão.
    """
    # Arrange
    student_mock_repository = MagicMock()
    course_mock_repository = MagicMock()
    student_mock_repository.get_student_by_id.return_value = student
    student_mock_repository.remove_student.return_value = True
    
    service = StudentDeletionService(
        student_repository=student_mock_repository, 
        course_repository=course_mock_repository
    )

    # Act
    result = service.delete_student(student)

    # Assert
    assert result == 'Sucesso ao deletar estudante.'
    student_mock_repository.get_student_by_id.assert_called_once_with(student.student_id)
    student_mock_repository.remove_student.assert_called_once_with(student.student_id)


def test_delete_student_fails_if_not_found(student: Student) -> None:
    """Garante que retorna falha e não tenta remover se o estudante não for achado.

    Impede chamadas de remoção em registros ausentes no arquivo de persistência.
    """
    # Arrange
    student_mock_repository = MagicMock()
    course_mock_repository = MagicMock()
    student_mock_repository.get_student_by_id.return_value = None
    
    service = StudentDeletionService(
        student_repository=student_mock_repository, 
        course_repository=course_mock_repository
    )

    # Act
    result = service.delete_student(student)

    # Assert
    assert result == 'Estudante não encontrado.'
    student_mock_repository.get_student_by_id.assert_called_once_with(student.student_id)
    student_mock_repository.remove_student.assert_not_called()


def test_delete_student_exception_handling(student: Student) -> None:
    """Garante que falhas internas ou de I/O na exclusão são tratadas com segurança.

    Verifica se erros imprevistos de gravação são capturados fornecendo uma 
    mensagem de erro tratada.
    """
    # Arrange
    student_mock_repository = MagicMock()
    course_mock_repository = MagicMock()
    student_mock_repository.get_student_by_id.side_effect = Exception("Disk I/O Error")
    
    service = StudentDeletionService(
        student_repository=student_mock_repository, 
        course_repository=course_mock_repository
    )

    # Act
    result = service.delete_student(student)

    # Assert
    assert result == 'Erro ao deletar estudante'
    student_mock_repository.remove_student.assert_not_called()


# ==============================================================================
# TESTES: ATUALIZAÇÃO DE ESTUDANTES (StudentUpdatableService)
# ==============================================================================

def test_update_student_success(student: Student) -> None:
    """Garante que o estudante é atualizado com sucesso se ele já existir na base.

    Verifica a execução feliz de salvamento de alterações cadastrais para entidades 
    previamente existentes.
    """
    # Arrange
    mock_repository = MagicMock()
    mock_repository.get_student_by_id.return_value = student
    mock_repository.update_student.return_value = True
    
    service = StudentUpdatableService(student_repository=mock_repository)

    # Act
    result = service.update_student(student)

    # Assert
    assert result == 'Sucesso ao atualizar estudante.'
    mock_repository.get_student_by_id.assert_called_once_with(student.student_id)
    mock_repository.update_student.assert_called_once_with(student)


def test_update_student_fails_if_not_found(student: Student) -> None:
    """Garante que o serviço recusa a atualização se o estudante não for achado.

    Impede mutações cadastrais em dados órfãos ou inconsistentes na persistência.
    """
    # Arrange
    mock_repository = MagicMock()
    mock_repository.get_student_by_id.return_value = None
    
    service = StudentUpdatableService(student_repository=mock_repository)

    # Act
    result = service.update_student(student)

    # Assert
    assert result == 'Estudante não encontrado.'
    mock_repository.get_student_by_id.assert_called_once_with(student.student_id)
    mock_repository.update_student.assert_not_called()


def test_update_student_exception_handling(student: Student) -> None:
    """Garante que falhas de infraestrutura ao atualizar retornam mensagem de erro.

    Assegura o tratamento de falhas como arquivos corrompidos ou bloqueios de gravação.
    """
    # Arrange
    mock_repository = MagicMock()
    mock_repository.get_student_by_id.side_effect = Exception("Database locked")
    
    service = StudentUpdatableService(student_repository=mock_repository)

    # Act
    result = service.update_student(student)

    # Assert
    assert result == 'Erro ao atualizar estudante'
    mock_repository.update_student.assert_not_called()
    service = StudentUpdatableService(student_repository=mock_repository)

    # Act
    result = service.update_student(student)

    # Assert
    assert result == 'Erro ao atualizar estudante'
    mock_repository.update_student.assert_not_called()

import pytest
from unittest.mock import MagicMock

from src import Student, StudentAdderService, StudentGetterByIdService, StudentGetterService, StudentDeletionService, StudentUpdatableService

@pytest.fixture
def student():
    """Fixture que fornece um objeto Student padrão para os testes do serviço."""
    return Student(name="Daniel", student_tax_id="123.456.789-00")

def test_add_student_success(student):
    """Garante que o estudante é adicionado com sucesso se o CPF não existir no sistema."""
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


def test_add_student_fails_when_student_already_exists(student):
    """Garante que o serviço barra a inserção se o CPF (tax_id) já estiver cadastrado."""
    # Arrange
    repository_mock = MagicMock()
    # Simula que já existe um estudante com esse mesmo CPF no banco
    repository_mock.get_student_by_tax_id.return_value = student

    service = StudentAdderService(student_repository=repository_mock)

    # Act
    result = service.add_student(student)

    # Assert
    assert result == 'Estudante já existe.'
    repository_mock.get_student_by_tax_id.assert_called_once_with(student.student_tax_id)
    # Garante estritamente que a tentativa de salvar NUNCA ocorreu
    repository_mock.add_student.assert_not_called()


def test_add_student_fails_when_repository_cannot_save(student):
    """Garante o retorno correto se o repositório falhar na operação física de salvamento."""
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


def test_add_student_exception_handling(student):
    """Garante que exceções e erros catastróficas inesperados são tratados pelo bloco try/except."""
    # Arrange
    repository_mock = MagicMock()
    repository_mock.get_student_by_tax_id.side_effect = Exception("Database connection timeout")

    service = StudentAdderService(student_repository=repository_mock)

    # Act
    result = service.add_student(student)

    # Assert
    assert result == "Erro ao adicionar estudante"
    repository_mock.add_student.assert_not_called()

def test_student_getter_by_id_success(student):
    """Garante que o serviço retorna o objeto Student correto quando o ID existe."""
    # Arrange
    student_mock_repository = MagicMock()
    course_mock_repository = MagicMock()

    student_mock_repository.get_student_by_id.return_value = student
    course_mock_repository.get_all_courses.return_value = []
    
    service = StudentGetterByIdService(student_repository=student_mock_repository,course_repository=course_mock_repository)

    # Act
    result = service.get_student_by_id(student)

    # Assert
    assert result is not None
    assert result.student_id == student.student_id
    assert result.name == student.name
    student_mock_repository.get_student_by_id.assert_called_once_with(student_id=student.student_id)
    course_mock_repository.get_all_courses.assert_called_once()

def test_student_getter_by_id_not_found():
    """Garante que o serviço retorna None se o ID não existir no repositório."""
    # Arrange
    student_mock_repository = MagicMock()
    course_mock_repository = MagicMock()

    student_mock_repository.get_student_by_id.return_value = None
    test_student = Student(name="Fake", student_tax_id="000.000.000-00")
    
    service = StudentGetterByIdService(student_repository=student_mock_repository, course_repository=course_mock_repository)

    # Act
    result = service.get_student_by_id(student=test_student)

    # Assert
    assert result is None
    student_mock_repository.get_student_by_id.assert_called_once_with(student_id=test_student.student_id)
    course_mock_repository.get_all_courses.assert_not_called()

def test_student_getter_by_id_exception_handling():
    """Garante que o serviço captura exceções do repositório de forma segura e retorna None."""
    # Arrange
    student_mock_repository = MagicMock()
    course_mock_repository = MagicMock()

    student_mock_repository.get_student_by_id.side_effect = Exception("File read error")
    
    service = StudentGetterByIdService(student_repository=student_mock_repository, course_repository=course_mock_repository)

    # Act
    result = service.get_student_by_id("qualquer-id")

    # Assert
    assert result is None

def test_student_getter_success(student):
    """Garante que o serviço retorna a lista completa de estudantes do repositório."""
    # Arrange
    student_mock_repository = MagicMock()
    course_mock_repository = MagicMock()
    s1 = student
    s2 = Student(name="Maria", student_tax_id="987.654.321-11")
    
    # Configura o mock do repositório para retornar uma lista com os dois estudantes
    student_mock_repository.get_all_students.return_value = [s1, s2]

    
    service = StudentGetterService(student_repository=student_mock_repository, course_repository=course_mock_repository)

    # Act
    result = service.get_all_students()

    # Assert
    assert len(result) == 2
    assert result[0].name == "Daniel"
    assert result[1].name == "Maria"
    student_mock_repository.get_all_students.assert_called_once()


def test_student_getter_returns_empty_list_when_no_students():
    """Garante que o serviço retorna uma lista vazia se não houver registros."""
    # Arrange
    student_mock_repository = MagicMock()
    course_mock_repository = MagicMock()
    student_mock_repository.get_all_students.return_value = []
    
    service = StudentGetterService(student_repository=student_mock_repository, course_repository=course_mock_repository)

    # Act
    result = service.get_all_students()

    # Assert
    assert result == []
    student_mock_repository.get_all_students.assert_called_once()


def test_student_getter_exception_handling():
    """Garante que o serviço captura falhas do repositório de forma segura e retorna uma lista vazia."""
    # Arrange
    student_mock_repository = MagicMock()
    course_mock_repository = MagicMock()
    # Simula um erro crítico ao acessar a infraestrutura (ex: arquivo corrompido)
    student_mock_repository.get_all_students.side_effect = Exception("IO Error")
    
    service = StudentGetterService(student_repository=student_mock_repository, course_repository=course_mock_repository)

    # Act
    result = service.get_all_students()

    # Assert
    assert result == []

def test_delete_student_success(student):
    """Garante que o estudante é removido com sucesso se existir na base."""
    # Arrange
    student_mock_repository = MagicMock()
    course_mock_repository = MagicMock()
    # O repositório simula que encontrou o estudante no banco
    student_mock_repository.get_student_by_id.return_value = student
    student_mock_repository.remove_student.return_value = True
    
    service = StudentDeletionService(student_repository=student_mock_repository, course_repository=course_mock_repository)

    # Act
    result = service.delete_student(student)

    # Assert
    assert result == 'Sucesso ao deletar estudante.'
    student_mock_repository.get_student_by_id.assert_called_once_with(student.student_id)
    student_mock_repository.remove_student.assert_called_once_with(student.student_id)


def test_delete_student_fails_if_not_found(student):
    """Garante que retorna False e não tenta remover se o estudante não for encontrado."""
    # Arrange
    student_mock_repository = MagicMock()
    course_mock_repository = MagicMock()
    # O repositório simula que não achou o ID informado
    student_mock_repository.get_student_by_id.return_value = None
    
    service = StudentDeletionService(student_repository=student_mock_repository, course_repository=course_mock_repository)

    # Act
    result = service.delete_student(student)

    # Assert
    assert result == 'Estudante não encontrado.'
    student_mock_repository.get_student_by_id.assert_called_once_with(student.student_id)
    # Garante de forma estrita que o método de deleção física nunca foi chamado
    student_mock_repository.remove_student.assert_not_called()


def test_delete_student_exception_handling(student):
    """Garante que falhas internas ou de conexão no repositório retornam False com segurança."""
    # Arrange
    student_mock_repository = MagicMock()
    course_mock_repository = MagicMock()
    # Força um erro de infraestrutura na primeira chamada
    student_mock_repository.get_student_by_id.side_effect = Exception("Disk I/O Error")
    
    service = StudentDeletionService(student_repository=student_mock_repository, course_repository=course_mock_repository)

    # Act
    result = service.delete_student(student)

    # Assert
    assert result == 'Erro ao deletar estudante'
    student_mock_repository.remove_student.assert_not_called()

def test_update_student_success(student):
    """Garante que o estudante é atualizado com sucesso se ele já existir na base."""
    # Arrange
    mock_repository = MagicMock()
    # O repositório simula que encontrou o estudante antigo na base de dados
    mock_repository.get_student_by_id.return_value = student
    mock_repository.update_student.return_value = True
    
    service = StudentUpdatableService(student_repository=mock_repository)

    # Act
    result = service.update_student(student)

    # Assert
    assert result == 'Sucesso ao atualizar estudante.'
    mock_repository.get_student_by_id.assert_called_once_with(student.student_id)
    mock_repository.update_student.assert_called_once_with(student)


def test_update_student_fails_if_not_found(student):
    """Garante que o serviço retorna False e cancela a operação se o estudante não existir."""
    # Arrange
    mock_repository = MagicMock()
    # O repositório simula que o estudante não foi localizado (retorna None)
    mock_repository.get_student_by_id.return_value = None
    
    service = StudentUpdatableService(student_repository=mock_repository)

    # Act
    result = service.update_student(student)

    # Assert
    assert result == 'Estudante não encontrado.'
    mock_repository.get_student_by_id.assert_called_once_with(student.student_id)
    # Garante que o repositório NUNCA tentou forçar uma atualização
    mock_repository.update_student.assert_not_called()


def test_update_student_exception_handling(student):
    """Garante que falhas de infraestrutura no repositório são tratadas e retornam False."""
    # Arrange
    mock_repository = MagicMock()
    # Força uma exceção simulando um travamento de leitura de arquivo ou banco fora do ar
    mock_repository.get_student_by_id.side_effect = Exception("Database locked")
    
    service = StudentUpdatableService(student_repository=mock_repository)

    # Act
    result = service.update_student(student)

    # Assert
    assert result == 'Erro ao atualizar estudante'
    mock_repository.update_student.assert_not_called()
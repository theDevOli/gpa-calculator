import pytest
from unittest.mock import MagicMock

from src import Student, StudentAdderService, StudentGetterByIdService, StudentGetterService, StudentDeletionService, StudentUpdatableService

@pytest.fixture
def student():
    """Fixture que fornece um objeto Student padrão para os testes do serviço."""
    return Student(name="Daniel", student_tax_id="123.456.789-00")

def test_student_adder_success(student):
    """Garante que o estudante é adicionado com sucesso quando o CPF não existe na base."""
    # Arrange
    mock_repository = MagicMock()
    # O CPF não existe, então o repositório deve retornar None na busca
    mock_repository.get_student_by_tax_id.return_value = None
    mock_repository.add_student.return_value = True
    
    service = StudentAdderService(student_repository=mock_repository)

    # Act
    result = service.add_student(student)

    # Assert
    assert result is True
    mock_repository.get_student_by_tax_id.assert_called_once_with(student.student_tax_id)
    mock_repository.add_student.assert_called_once_with(student)

def test_student_adder_fails_when_tax_id_already_exists(student):
    """Garante que o serviço retorna False e não adiciona se o CPF já estiver cadastrado."""
    # Arrange
    mock_repository = MagicMock()
    # Simula que o estudante já existe retornando um objeto qualquer (ou o próprio mock)
    mock_repository.get_student_by_tax_id.return_value = student
    
    service = StudentAdderService(student_repository=mock_repository)

    # Act
    result = service.add_student(student)

    # Assert
    assert result is False
    mock_repository.get_student_by_tax_id.assert_called_once_with(student.student_tax_id)
    # Garante que o repositório NUNCA tentou salvar o registro duplicado
    mock_repository.add_student.assert_not_called()

def test_student_adder_exception_handling(student):
    """Garante que o serviço trata exceções do repositório de forma segura e retorna False."""
    # Arrange
    mock_repository = MagicMock()
    # Força uma exceção inesperada logo na primeira consulta ao banco/arquivo
    mock_repository.get_student_by_tax_id.side_effect = Exception("Connection failed")
    
    service = StudentAdderService(student_repository=mock_repository)

    # Act
    result = service.add_student(student)

    # Assert
    assert result is False
    mock_repository.add_student.assert_not_called()

def test_student_getter_by_id_success(student):
    """Garante que o serviço retorna o objeto Student correto quando o ID existe."""
    # Arrange
    mock_repository = MagicMock()
    # O repositório finge encontrar o estudante e retorna o objeto dele
    mock_repository.get_student_by_id.return_value = student
    
    service = StudentGetterByIdService(student_repository=mock_repository)

    # Act
    result = service.get_student_by_id(student)

    # Assert
    assert result is not None
    assert result.student_id == student.student_id
    assert result.name == student.name
    mock_repository.get_student_by_id.assert_called_once_with(student.student_id)

def test_student_getter_by_id_not_found():
    """Garante que o serviço retorna None se o ID não existir no repositório."""
    # Arrange
    mock_repository = MagicMock()
    # Simula que o repositório não achou ninguém (retorna None)
    mock_repository.get_student_by_id.return_value = None
    test_student = Student(name="Fake", student_tax_id="000.000.000-00")
    
    service = StudentGetterByIdService(student_repository=mock_repository)

    # Act
    result = service.get_student_by_id(student=test_student)

    # Assert
    assert result is None
    mock_repository.get_student_by_id.assert_called_once_with(test_student.student_id)

def test_student_getter_by_id_exception_handling():
    """Garante que o serviço captura exceções do repositório de forma segura e retorna None."""
    # Arrange
    mock_repository = MagicMock()
    # Força um erro inesperado no repositório (ex: arquivo corrompido)
    mock_repository.get_student_by_id.side_effect = Exception("File read error")
    
    service = StudentGetterByIdService(student_repository=mock_repository)

    # Act
    result = service.get_student_by_id("qualquer-id")

    # Assert
    assert result is None

def test_student_getter_success(student):
    """Garante que o serviço retorna a lista completa de estudantes do repositório."""
    # Arrange
    mock_repository = MagicMock()
    s1 = student
    s2 = Student(name="Maria", student_tax_id="987.654.321-11")
    
    # Configura o mock do repositório para retornar uma lista com os dois estudantes
    mock_repository.get_all_students.return_value = [s1, s2]
    
    service = StudentGetterService(student_repository=mock_repository)

    # Act
    result = service.get_all_students()

    # Assert
    assert len(result) == 2
    assert result[0].name == "Daniel"
    assert result[1].name == "Maria"
    mock_repository.get_all_students.assert_called_once()


def test_student_getter_returns_empty_list_when_no_students():
    """Garante que o serviço retorna uma lista vazia se não houver registros."""
    # Arrange
    mock_repository = MagicMock()
    mock_repository.get_all_students.return_value = []
    
    service = StudentGetterService(student_repository=mock_repository)

    # Act
    result = service.get_all_students()

    # Assert
    assert result == []
    mock_repository.get_all_students.assert_called_once()


def test_student_getter_exception_handling():
    """Garante que o serviço captura falhas do repositório de forma segura e retorna uma lista vazia."""
    # Arrange
    mock_repository = MagicMock()
    # Simula um erro crítico ao acessar a infraestrutura (ex: arquivo corrompido)
    mock_repository.get_all_students.side_effect = Exception("IO Error")
    
    service = StudentGetterService(student_repository=mock_repository)

    # Act
    result = service.get_all_students()

    # Assert
    assert result == []

def test_delete_student_success(student):
    """Garante que o estudante é removido com sucesso se existir na base."""
    # Arrange
    mock_repository = MagicMock()
    # O repositório simula que encontrou o estudante no banco
    mock_repository.get_student_by_id.return_value = student
    mock_repository.remove_student.return_value = True
    
    service = StudentDeletionService(student_repository=mock_repository)

    # Act
    result = service.delete_student(student)

    # Assert
    assert result is True
    mock_repository.get_student_by_id.assert_called_once_with(student.student_id)
    mock_repository.remove_student.assert_called_once_with(student.student_id)


def test_delete_student_fails_if_not_found(student):
    """Garante que retorna False e não tenta remover se o estudante não for encontrado."""
    # Arrange
    mock_repository = MagicMock()
    # O repositório simula que não achou o ID informado
    mock_repository.get_student_by_id.return_value = None
    
    service = StudentDeletionService(student_repository=mock_repository)

    # Act
    result = service.delete_student(student)

    # Assert
    assert result is False
    mock_repository.get_student_by_id.assert_called_once_with(student.student_id)
    # Garante de forma estrita que o método de deleção física nunca foi chamado
    mock_repository.remove_student.assert_not_called()


def test_delete_student_exception_handling(student):
    """Garante que falhas internas ou de conexão no repositório retornam False com segurança."""
    # Arrange
    mock_repository = MagicMock()
    # Força um erro de infraestrutura na primeira chamada
    mock_repository.get_student_by_id.side_effect = Exception("Disk I/O Error")
    
    service = StudentDeletionService(student_repository=mock_repository)

    # Act
    result = service.delete_student(student)

    # Assert
    assert result is False
    mock_repository.remove_student.assert_not_called()

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
    assert result is True
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
    assert result is False
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
    assert result is False
    mock_repository.update_student.assert_not_called()
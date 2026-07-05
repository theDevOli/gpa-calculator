import uuid
import pytest
from unittest.mock import MagicMock

from src import Student
from src import StudentRepository


@pytest.fixture
def student():
    """Fixture que fornece um objeto Student padrão com CPF para os testes."""
    # Certifique-se de que a sua entidade Student aceita o tax_id no construtor
    return Student(name="Daniel", student_tax_id="123.456.789-00")


def test_student_generates_uuid():
    """Garante que a entidade Student gera um UUID válido em sua inicialização."""
    student = Student("Daniel", "123.456.789-00")

    uuid_obj = uuid.UUID(student.student_id)

    assert str(uuid_obj) == student.student_id


def test_add_student(student):
    """Garante que o repositório salva corretamente a string CSV do estudante."""
    mock_context = MagicMock()
    repository = StudentRepository(context=mock_context)

    result = repository.add_student(student)

    mock_context.save_entity.assert_called_once_with(student.to_csv())
    assert result is True


def test_add_student_exception(student):
    """Garante que o método retorna False caso ocorra uma falha no contexto ao salvar."""
    mock_context = MagicMock()
    mock_context.save_entity.side_effect = Exception("Database error")
    repository = StudentRepository(context=mock_context)

    result = repository.add_student(student)

    assert result is False


def test_get_student_by_id(student):
    """Garante que o estudante é retornado corretamente quando localizado pelo ID."""
    mock_context = MagicMock()
    mock_context.get_all_entities.return_value = [student.to_csv()]
    repository = StudentRepository(context=mock_context)

    result = repository.get_student_by_id(student.student_id)

    assert result is not None
    assert result.student_id == student.student_id
    assert result.name == student.name


def test_get_student_by_id_not_found():
    """Garante que retorna None quando o ID buscado não existe no arquivo."""
    mock_context = MagicMock()
    mock_context.get_all_entities.return_value = []
    repository = StudentRepository(context=mock_context)

    result = repository.get_student_by_id(str(uuid.uuid4()))

    assert result is None


def test_get_student_by_tax_id(student):
    """Garante que o estudante é retornado com sucesso ao ser buscado pelo CPF (tax_id)."""
    mock_context = MagicMock()
    mock_context.get_all_entities.return_value = [student.to_csv()]
    repository = StudentRepository(context=mock_context)

    # Buscando usando o CPF da fixture
    result = repository.get_student_by_tax_id("123.456.789-00")

    assert result is not None
    assert result.student_id == student.student_id
    # Dependendo de como seu Student.from_csv foi feito, valide o tax_id aqui também se desejar
    assert result.name == student.name


def test_get_student_by_tax_id_not_found():
    """Garante que retorna None quando o CPF buscado não existe no arquivo."""
    mock_context = MagicMock()
    mock_context.get_all_entities.return_value = [
        "some-id,Daniel,123.456.789-00,[]"
    ]
    repository = StudentRepository(context=mock_context)

    # Buscando por um CPF que não está mapeado na lista acima
    result = repository.get_student_by_tax_id("000.000.000-11")

    assert result is None


def test_get_all_students():
    """Garante que todos os estudantes válidos do arquivo são listados em objetos."""
    mock_context = MagicMock()
    s1 = Student("Daniel", "123.456.789-00")
    s2 = Student("Maria", "987.654.321-11")
    
    # Adicionamos uma string vazia no meio para testar a nossa nova proteção antiquebra do repositório
    mock_context.get_all_entities.return_value = [s1.to_csv(), "   \n", s2.to_csv()]
    
    repository = StudentRepository(context=mock_context)

    result = repository.get_all_students()

    assert len(result) == 2
    assert result[0].student_id == s1.student_id
    assert result[0].name == s1.name
    assert result[1].student_id == s2.student_id
    assert result[1].name == s2.name


def test_update_student(student):
    """Garante que a atualização envia a string CSV e o ID corretos ao contexto."""
    mock_context = MagicMock()
    repository = StudentRepository(context=mock_context)

    result = repository.update_student(student)

    mock_context.update_entity.assert_called_once_with(
        student.to_csv(), student.student_id
    )
    assert result is True


def test_update_student_exception(student):
    """Garante que retorna False caso ocorra erro no contexto durante a atualização."""
    mock_context = MagicMock()
    mock_context.update_entity.side_effect = Exception("Database error")
    repository = StudentRepository(context=mock_context)

    result = repository.update_student(student)

    assert result is False


def test_remove_student(student):
    """Garante que a exclusão repassa o ID correto para o contexto."""
    mock_context = MagicMock()
    repository = StudentRepository(context=mock_context)

    result = repository.remove_student(student.student_id)

    mock_context.remove_entity.assert_called_once_with(student.student_id)
    assert result is True


def test_remove_student_exception(student):
    """Garante que retorna False caso ocorra uma falha de banco/escrita na remoção."""
    mock_context = MagicMock()
    mock_context.remove_entity.side_effect = Exception("Database error")
    repository = StudentRepository(context=mock_context)

    result = repository.remove_student(student.student_id)

    assert result is False
"""Módulo de testes unitários para a classe StudentRepository e a entidade Student.

Este módulo contém cenários de testes automatizados que validam o comportamento 
das operações de persistência e manipulação (CRUD) aplicadas à entidade Student, 
garantindo a resiliência a falhas de banco de dados e a correta desserialização 
de dados a partir de mocks de arquivos CSV.
"""

import uuid
import pytest
from unittest.mock import MagicMock

from src import Student
from src import StudentRepository


@pytest.fixture
def student() -> Student:
    """Fixture que fornece um objeto Student padrão com CPF para os testes.

    Garante uma instância de teste pré-configurada para reutilização em múltiplos 
    cenários do repositório.

    Returns:
        Student: Uma instância contendo dados de teste da entidade Student.
    """
    return Student(name="Daniel", student_tax_id="123.456.789-00")


def test_student_generates_uuid() -> None:
    """Garante que a entidade Student gera um UUID válido em sua inicialização.

    Valida se a string identificadora gerada pelo modelo pode ser convertida 
    com sucesso para um objeto UUID nativo do Python sem lançar erros de formato.
    """
    student = Student("Daniel", "123.456.789-00")

    uuid_obj = uuid.UUID(student.student_id)

    assert str(uuid_obj) == student.student_id


def test_add_student(student: Student) -> None:
    """Garante que o repositório salva corretamente a string CSV do estudante.

    Verifica se a chamada ao método de gravação física (`save_entity`) do contexto 
    é invocada exatamente uma vez com a linha formatada e se retorna verdadeiro.
    """
    mock_context = MagicMock()
    repository = StudentRepository(context=mock_context)

    result = repository.add_student(student)

    mock_context.save_entity.assert_called_once_with(student.to_csv())
    assert result is True


def test_add_student_exception(student: Student) -> None:
    """Garante que o método retorna False caso ocorra uma falha no contexto ao salvar.

    Valida se exceções disparadas pelo contexto de gravação em disco são capturadas 
    e convertidas em um retorno falso e limpo pelo repositório.
    """
    mock_context = MagicMock()
    mock_context.save_entity.side_effect = Exception("Database error")
    repository = StudentRepository(context=mock_context)

    result = repository.add_student(student)

    assert result is False


def test_get_student_by_id(student: Student) -> None:
    """Garante que o estudante é retornado corretamente quando localizado pelo ID.

    Testa se o repositório sabe filtrar a lista bruta de registros e reconstruir 
    fielmente a instância de `Student` com as propriedades corretas.
    """
    mock_context = MagicMock()
    mock_context.get_all_entities.return_value = [student.to_csv()]
    repository = StudentRepository(context=mock_context)

    result = repository.get_student_by_id(student.student_id)

    assert result is not None
    assert result.student_id == student.student_id
    assert result.name == student.name


def test_get_student_by_id_not_found() -> None:
    """Garante que retorna None quando o ID buscado não existe no arquivo.

    Valida a robustez ao tentar acessar registros de identificadores inexistentes, 
    verificando se o resultado é nulo.
    """
    mock_context = MagicMock()
    mock_context.get_all_entities.return_value = []
    repository = StudentRepository(context=mock_context)

    result = repository.get_student_by_id(str(uuid.uuid4()))

    assert result is None


def test_get_student_by_tax_id(student: Student) -> None:
    """Garante que o estudante é retornado com sucesso ao ser buscado pelo CPF (tax_id).

    Certifica o fluxo de busca de estudantes por documentos secundários únicos e a 
    correta localização do registro no repositório.
    """
    mock_context = MagicMock()
    mock_context.get_all_entities.return_value = [
        student.to_csv()
    ]
    repository = StudentRepository(context=mock_context)

    # Buscando usando o CPF da fixture
    result = repository.get_student_by_tax_id(student.student_tax_id)

    assert result is not None
    assert result.student_id == student.student_id
    assert result.name == student.name


def test_get_student_by_tax_id_not_found() -> None:
    """Garante que retorna None quando o CPF buscado não existe no arquivo.

    Valida o comportamento de proteção quando o repositório filtra as entidades 
    mas não encontra nenhuma correspondência de CPF.
    """
    mock_context = MagicMock()
    mock_context.get_all_entities.return_value = [
        "some-id,Daniel,123.456.789-00,[]"
    ]
    repository = StudentRepository(context=mock_context)

    # Buscando por um CPF que não está mapeado na lista acima
    result = repository.get_student_by_tax_id("000.000.000-11")

    assert result is None


def test_get_all_students() -> None:
    """Garante que todos os estudantes válidos do arquivo são listados em objetos.

    Assegura que quebras de linha em branco ou linhas mal formatadas/vazias não 
    geram erros de processamento (*parsing*) no repositório.
    """
    mock_context = MagicMock()
    s1 = Student("Daniel", "123.456.789-00")
    s2 = Student("Maria", "987.654.321-11")
    
    # Adicionamos uma string vazia no meio para testar a nova proteção antiquebra do repositório
    mock_context.get_all_entities.return_value = [s1.to_csv(), "   \n", s2.to_csv()]
    
    repository = StudentRepository(context=mock_context)

    result = repository.get_all_students()

    assert len(result) == 2
    assert result[0].student_id == s1.student_id
    assert result[0].name == s1.name
    assert result[1].student_id == s2.student_id
    assert result[1].name == s2.name


def test_update_student(student: Student) -> None:
    """Garante que a atualização envia a string CSV e o ID corretos ao contexto.

    Verifica se os parâmetros de atualização física (`update_entity`) recebem 
    adequadamente os novos dados serializados e o ID correspondente à linha.
    """
    mock_context = MagicMock()
    repository = StudentRepository(context=mock_context)

    result = repository.update_student(student)

    mock_context.update_entity.assert_called_once_with(
        student.to_csv(), student.student_id
    )
    assert result is True


def test_update_student_exception(student: Student) -> None:
    """Garante que retorna False caso ocorra erro no contexto durante a atualização.

    Impede que exceções geradas por falhas físicas de arquivo ou concorrência de 
    escrita quebrem a execução da aplicação.
    """
    mock_context = MagicMock()
    mock_context.update_entity.side_effect = Exception("Database error")
    repository = StudentRepository(context=mock_context)

    result = repository.update_student(student)

    assert result is False


def test_remove_student(student: Student) -> None:
    """Garante que a exclusão repassa o ID correto para o contexto.

    Valida se a instrução de remoção é devidamente repassada à camada física com 
    o ID correto do estudante selecionado.
    """
    mock_context = MagicMock()
    repository = StudentRepository(context=mock_context)

    result = repository.remove_student(student.student_id)

    mock_context.remove_entity.assert_called_once_with(student.student_id)
    assert result is True


def test_remove_student_exception(student: Student) -> None:
    """Garante que retorna False caso ocorra uma falha de banco/escrita na remoção.

    Assegura o tratamento gracioso de exceções de exclusão na infraestrutura, 
    retornando False.
    """
    mock_context = MagicMock()
    mock_context.remove_entity.side_effect = Exception("Database error")
    repository = StudentRepository(context=mock_context)

    result = repository.remove_student(student.student_id)

    assert result is False

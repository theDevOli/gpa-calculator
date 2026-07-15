import uuid
"""Módulo de testes unitários para a classe CourseRepository e a entidade Course.

Este módulo contém os testes responsáveis por garantir o correto funcionamento do
repositório de cursos, cobrindo operações de criação, leitura, atualização e
exclusão (CRUD), bem como o tratamento de exceções simuladas via mocks.
"""

import uuid
import pytest
from unittest.mock import MagicMock

from src import Course, CourseRepository


@pytest.fixture
def course() -> Course:
    """Fixture que fornece uma instância padrão da entidade Course para os testes.

    Returns:
        Course: Uma instância pré-configurada da classe Course.
    """
    return Course("Math", 4, 9.8)


def test_course_generates_uuid() -> None:
    """Garante que um novo curso gera automaticamente um identificador único (UUID).

    Verifica se o atributo `course_id` é inicializado corretamente como uma string
    não nula.
    """
    course = Course("Math", 4, 9.8)

    course_id = course.course_id

    assert course_id is not None
    assert isinstance(course_id, str)


def test_add_course(course: Course) -> None:
    """Garante que a adição de um curso é realizada com sucesso no repositório.

    Verifica se o método de persistência do contexto (`save_entity`) é chamado 
    corretamente com a representação em CSV da entidade e se o retorno indica sucesso.
    """
    mock_context = MagicMock()
    repository = CourseRepository(context=mock_context)

    result = repository.add_course(course)

    mock_context.save_entity.assert_called_once_with(course.to_csv())
    assert result is True


def test_add_course_exception(course: Course) -> None:
    """Garante que falhas na persistência ao adicionar um curso retornam False.

    Simula uma exceção lançada pelo banco de dados/contexto de persistência e 
    assegura que o repositório trata o erro graciosamente, retornando False.
    """
    mock_context = MagicMock()
    mock_context.save_entity.side_effect = Exception("DB error")
    repository = CourseRepository(context=mock_context)

    result = repository.add_course(course)

    assert result is False


def test_get_course_by_id(course: Course) -> None:
    """Garante que é possível recuperar um curso existente buscando pelo seu ID.

    Verifica se o repositório lê o contexto de persistência, localiza a linha 
    referente ao curso e reconstitui o objeto `Course` corretamente.
    """
    mock_context = MagicMock()
    mock_context.get_all_entities.return_value = [course.to_csv()]
    repository = CourseRepository(context=mock_context)

    result = repository.get_course_by_id(course.course_id)

    assert result is not None
    assert result.course_id == course.course_id
    assert result.name == course.name


def test_get_course_by_id_not_found() -> None:
    """Garante que buscar por um ID inexistente retorna None.

    Verifica o comportamento do repositório quando o ID buscado não consta
    nos registros retornados pelo contexto de persistência.
    """
    mock_context = MagicMock()
    mock_context.get_all_entities.return_value = []
    repository = CourseRepository(context=mock_context)

    result = repository.get_course_by_id(str(uuid.uuid4()))

    assert result is None


def test_get_all_courses() -> None:
    """Garante que o repositório retorna a lista completa de todos os cursos persistidos.

    Verifica a correta desserialização e mapeamento de múltiplas linhas de CSV para
    uma lista contendo as instâncias correspondentes de `Course`.
    """
    mock_context = MagicMock()
    c1 = Course("Math", 4, 9.8)
    c2 = Course("Physics", 3, 8.5)
    mock_context.get_all_entities.return_value = [c1.to_csv(), c2.to_csv()]
    
    repository = CourseRepository(context=mock_context)

    result = repository.get_all_courses()

    assert len(result) == 2
    assert result[0].course_id == c1.course_id
    assert result[0].name == c1.name
    assert result[1].course_id == c2.course_id
    assert result[1].name == c2.name


def test_update_course(course: Course) -> None:
    """Garante que a atualização de um curso é realizada com sucesso no repositório.

    Verifica se o método `update_entity` do contexto é acionado passando a nova 
    representação dos dados e o ID do curso em questão, retornando True.
    """
    mock_context = MagicMock()
    repository = CourseRepository(context=mock_context)

    result = repository.update_course(course)

    mock_context.update_entity.assert_called_once_with(
        course.to_csv(), course.course_id
    )
    assert result is True


def test_update_course_exception(course: Course) -> None:
    """Garante que falhas ao tentar atualizar um curso retornam False.

    Simula um erro durante a atualização no arquivo físico de dados e verifica 
    se o repositório lida com a exceção retornando False.
    """
    mock_context = MagicMock()
    mock_context.update_entity.side_effect = Exception("DB error")
    repository = CourseRepository(context=mock_context)

    result = repository.update_course(course)

    assert result is False


def test_remove_course(course: Course) -> None:
    """Garante que a remoção de um curso ocorre com sucesso através do ID.

    Verifica se o método `remove_entity` do contexto é acionado com o ID correto 
    do curso e se a operação reporta sucesso (True).
    """
    mock_context = MagicMock()
    repository = CourseRepository(context=mock_context)

    result = repository.remove_course(course.course_id)

    mock_context.remove_entity.assert_called_once_with(course.course_id)
    assert result is True


def test_remove_course_exception(course: Course) -> None:
    """Garante que falhas ao tentar remover um curso retornam False.

    Simula um erro durante o processo de remoção na persistência e assegura que 
    o repositório encapsula o erro, retornando False.
    """
    mock_context = MagicMock()
    mock_context.remove_entity.side_effect = Exception("DB error")
    repository = CourseRepository(context=mock_context)

    result = repository.remove_course(course.course_id)

    assert result is False

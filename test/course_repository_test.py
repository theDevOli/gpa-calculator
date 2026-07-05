import uuid
import pytest
from unittest.mock import MagicMock

from src import Course, CourseRepository


@pytest.fixture
def course():
    return Course("Math", 4, 9.8)


def test_course_generates_uuid():
    course = Course("Math", 4, 9.8)

    course_id = course.course_id

    assert course_id is not None
    assert isinstance(course_id, str)

def test_add_course(course):
    mock_context = MagicMock()
    repository = CourseRepository(context=mock_context)

    result = repository.add_course(course)

    mock_context.save_entity.assert_called_once_with(course.to_csv())
    assert result is True


def test_add_course_exception(course):
    mock_context = MagicMock()
    mock_context.save_entity.side_effect = Exception("DB error")
    repository = CourseRepository(context=mock_context)

    result = repository.add_course(course)

    assert result is False

def test_get_course_by_id(course):
    mock_context = MagicMock()
    mock_context.get_all_entities.return_value = [course.to_csv()]
    repository = CourseRepository(context=mock_context)

    result = repository.get_course_by_id(course.course_id)

    assert result is not None
    assert result.course_id == course.course_id
    assert result.name == course.name

def test_get_course_by_id_not_found():
    mock_context = MagicMock()
    mock_context.get_all_entities.return_value = []
    repository = CourseRepository(context=mock_context)

    result = repository.get_course_by_id(str(uuid.uuid4()))

    assert result is None

def test_get_all_courses():
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

def test_update_course(course):
    mock_context = MagicMock()
    repository = CourseRepository(context=mock_context)

    result = repository.update_course(course)

    mock_context.update_entity.assert_called_once_with(
        course.to_csv(), course.course_id
    )
    assert result is True

def test_update_course_exception(course):
    mock_context = MagicMock()
    mock_context.update_entity.side_effect = Exception("DB error")
    repository = CourseRepository(context=mock_context)

    result = repository.update_course(course)

    assert result is False

def test_remove_course(course):
    mock_context = MagicMock()
    repository = CourseRepository(context=mock_context)

    result = repository.remove_course(course.course_id)

    mock_context.remove_entity.assert_called_once_with(course.course_id)
    assert result is True

def test_remove_course_exception(course):
    mock_context = MagicMock()
    mock_context.remove_entity.side_effect = Exception("DB error")
    repository = CourseRepository(context=mock_context)

    result = repository.remove_course(course.course_id)

    assert result is False
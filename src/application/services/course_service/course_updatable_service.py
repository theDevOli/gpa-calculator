from src.domain.entities.course import Course
from src.domain.repository_contract.course_repository_contract import CourseRepositoryContract
from src.application.services_contract.course_contract.course_updatable_contract import CourseUpdatableContract

class CourseUpdatableService(CourseUpdatableContract):
    def __init__(self, course_repository: CourseRepositoryContract):
        self._repository = course_repository

    def update_course(self, to_update_course: Course) -> str:
        try:
            courses = self._repository.get_all_courses()
            existing_course = list(filter(lambda c: c.name == to_update_course.name, courses))

            if not existing_course:
                return 'Curso nao encontrado.'

            was_updated = self._repository.update_course(to_update_course)
            if not was_updated:
                return 'Nao foi possivel atualizar o curso.'
            
            return "Curso atualizado com sucesso."
        except Exception as e:
            print(f"Error updating course: {e}")
            return "Erro ao atualizar curso"

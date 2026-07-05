from src.domain.entities.course import Course
from src.domain.repository_contract.course_repository_contract import CourseRepositoryContract
from src.application.services_contract.course_contract.course_updatable_contract import CourseUpdatableContract

class CourseUpdatableService(CourseUpdatableContract):
    def __init__(self, course_repository: CourseRepositoryContract):
        self._repository = course_repository

    def update_course(self, to_update_course: Course) -> str:
        try:
            existing_course = self._repository.get_course_by_id(to_update_course.course_id)

            if existing_course is None:
                return 'Curso nao encontrado.'
            
            was_updated = self._repository.update_course(to_update_course)
            if not was_updated:
                return 'Nao foi possivel atualizar o curso.'
            
            return "Curso atualizado com sucesso."
        except Exception as e:
            print(f"Error updating course: {e}")
            return "Erro ao atualizar curso"

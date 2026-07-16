from flask import Flask, request, render_template, redirect, url_for

from src.domain.entities.course import Course 

from src.application.services_contract.course_contract.course_adder_contract import CourseAdderContract
from src.application.services_contract.course_contract.course_getter_contract import CourseGetterContract
from src.application.services_contract.course_contract.course_updatable_contract import CourseUpdatableContract
from src.application.services_contract.course_contract.course_deletion_contract import CourseDeletionContract

class CourseController:
    """Controlador responsável por expor as rotas HTTP relacionadas a Cursos.

    Esta classe atua como um adaptador de entrega (Delivery Mechanism) na arquitetura, 
    mapeando endpoints HTTP do Flask para os respectivos casos de uso (contracts) 
    do domínio de aplicação de cursos.

    Attributes:
        app (Flask): Instância do aplicativo Flask onde as rotas serão registradas.
        _course_getter (CourseGetterContract): Caso de uso para recuperação de cursos.
        _course_adder (CourseAdderContract): Caso de uso para criação e associação de cursos.
        _course_updatable (CourseUpdatableContract): Caso de uso para atualização de cursos.
        _course_deletion (CourseDeletionContract): Caso de uso para remoção de cursos.
    """

    def __init__(
            self,
            app: Flask,
            courser_getter: CourseGetterContract,
            course_adder: CourseAdderContract,
            course_updatable: CourseUpdatableContract,
            course_deletion: CourseDeletionContract
        ):
        """Inicializa o controlador de cursos e registra suas rotas no Flask.

        Args:
            app (Flask): Instância do Flask.
            courser_getter (CourseGetterContract): Serviço que busca as listagens de cursos.
            course_adder (CourseAdderContract): Serviço que gerencia adição de novos cursos.
            course_updatable (CourseUpdatableContract): Serviço que atualiza informações do curso.
            course_deletion (CourseDeletionContract): Serviço que lida com a deleção de cursos.
        """
        self.app = app
        self._course_getter = courser_getter
        self._course_adder = course_adder
        self._course_updatable = course_updatable
        self._course_deletion = course_deletion
        
        self._register_routes()

    def _register_routes(self) -> None:
        """Registra internamente os endpoints HTTP do Flask e seus manipuladores de rota.

        Este método define quatro rotas no aplicativo Flask:
        
        1.  **GET `/courses`** (`view_courses`): 
            Renderiza a página principal com a listagem geral de cursos cadastrados.
            
        2.  **POST `/students/<student_id>/courses`** (`add_course`): 
            Recebe dados do formulário de criação de curso e os associa ao estudante fornecido.
            Redireciona para a visualização dos cursos do estudante com uma mensagem de resultado.
            
        3.  **POST `/students/<student_id>/courses/<course_id>/update`** (`update_course`): 
            Atualiza as propriedades do curso no repositório através de dados vindos do formulário.
            Redireciona para a visualização de cursos do estudante informando o sucesso ou falha.
            
        4.  **POST `/students/<student_id>/courses/<course_id>/delete`** (`delete_course`): 
            Remove a entidade de curso com base no ID fornecido e limpa sua referência no estudante.
            Redireciona o usuário para a página de cursos do estudante.
        """
        
        @self.app.route("/courses", methods=["GET"])
        def view_courses():
            try:
                courses_list = self._course_getter.get_all_courses()
                return render_template("courses.html", courses=courses_list)
            except Exception as e:
                print(f"Erro ao listar cursos: {e}")
                return render_template("courses.html", courses=[])
            
        @self.app.route("/students/<student_id>/courses", methods=["POST"])
        def add_course(student_id):
            try:
                name = request.form.get("name")
                credit_hours = request.form.get("credit_hours")
                grade = request.form.get("grade")

                if name and credit_hours and grade:
                    new_course = Course(
                        name=name, 
                        credit_hours=int(credit_hours), 
                        grade=float(grade)
                    )
                    print(new_course.course_id)
                    msg = self._course_adder.add_course(student_id,new_course)
                    
                return redirect(url_for("view_student_courses", student_id=student_id,msg=msg))
            except Exception as e:
                print(f"Error add course: {e}")
                return redirect(url_for("view_student_courses", student_id=student_id, msg="Erro ao adicionar curso"))

        @self.app.route("/students/<student_id>/courses/<course_id>/update", methods=["POST"])
        def update_course(student_id, course_id):
            try:
                name = request.form.get("name")
                credit_hours = request.form.get("credit_hours")
                grade = request.form.get("grade")

                updated_course = Course(
                        course_id=course_id,
                        name=name, 
                        credit_hours=int(credit_hours), 
                        grade=float(grade)
                )
                msg = self._course_updatable.update_course(updated_course)

                return redirect(url_for("view_student_courses", student_id=student_id, msg=msg))
            except Exception as e:
                print(f"Error update course: {e}")
                return redirect(url_for("view_student_courses", student_id=student_id, msg="Erro ao atualizar curso"))

        @self.app.route("/students/<student_id>/courses/<course_id>/delete", methods=["POST"])
        def delete_course( student_id, course_id):
            try:
                deleted_course = Course(
                            course_id=course_id,
                            name="Placeholder", 
                            credit_hours=0, 
                            grade=0.0
                        )
                msg = self._course_deletion.delete_course(student_id=student_id,course=deleted_course)   
            
                return redirect(url_for("view_student_courses", student_id=student_id, msg=msg))
            except Exception as e:
                print(f"Error delete course: {e}")
                return redirect(url_for("view_student_courses", student_id=student_id, msg="Erro ao deletar curso"))
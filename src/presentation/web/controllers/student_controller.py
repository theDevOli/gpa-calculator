from flask import Flask, render_template, request, redirect, url_for

from src.domain.entities.student import Student
from src.application.services_contract.student_contract.student_getter_contract import StudentGetterContract
from src.application.services_contract.student_contract.student_getter_by_id_contract import StudentGetterByIdContract
from src.application.services_contract.student_contract.student_adder_contract import StudentAdderContract
from src.application.services_contract.student_contract.student_deletion_contract import StudentDeletionContract
from src.application.services_contract.student_contract.student_updatable_contract import StudentUpdatableContract


class StudentController:
    """Controlador responsável por expor as rotas HTTP relacionadas a Estudantes.

    Esta classe mapeia as requisições HTTP do Flask destinadas à gestão de estudantes,
    orquestrando as chamadas para os contratos de aplicação (casos de uso) correspondentes 
    e retornando as respectivas views renderizadas ou redirecionamentos de rotas.

    Attributes:
        app (Flask): Instância do aplicativo Flask onde as rotas serão registradas.
        _student_getter (StudentGetterContract): Caso de uso para listagem geral de estudantes.
        _student_getter_by_id (StudentGetterByIdContract): Caso de uso para consulta de estudante por ID.
        _student_adder (StudentAdderContract): Caso de uso para cadastro de estudantes.
        _student_deletion (StudentDeletionContract): Caso de uso para exclusão de estudantes.
        _student_updater (StudentUpdatableContract): Caso de uso para atualização de dados do estudante.
    """

    def __init__(
            self,
            app: Flask,
            student_getter: StudentGetterContract,
            student_getter_by_id: StudentGetterByIdContract,
            student_adder: StudentAdderContract,
            student_deletion: StudentDeletionContract,
            student_updater: StudentUpdatableContract
        ):
        """Inicializa o controlador de estudantes e registra as suas rotas no Flask.

        Args:
            app (Flask): Instância ativa do framework Flask.
            student_getter (StudentGetterContract): Serviço que busca listagens de estudantes.
            student_getter_by_id (StudentGetterByIdContract): Serviço que busca estudantes específicos pelo ID.
            student_adder (StudentAdderContract): Serviço de criação de estudantes.
            student_deletion (StudentDeletionContract): Serviço de remoção de estudantes.
            student_updater (StudentUpdatableContract): Serviço de atualização de cadastro de estudantes.
        """
        self.app = app
        self._student_getter = student_getter
        self._student_getter_by_id = student_getter_by_id
        self._student_adder = student_adder
        self._student_deletion = student_deletion
        self._student_updater = student_updater
        self._register_routes()

    def _register_routes(self) -> None:
        """Registra internamente os endpoints HTTP do Flask para o recurso de Estudante.

        Este método mapeia cinco rotas específicas:

        1.  **GET `/students`** (`view_students`): 
            Renderiza o painel principal (`students.html`) listando todos os estudantes cadastrados.
            
        2.  **POST `/students/add`** (`add_student`): 
            Coleta os parâmetros do formulário (`name` e `student_tax_id`) para cadastrar um novo 
            estudante e redireciona o usuário de volta para a rota de listagem geral.
            
        3.  **POST `/students/delete/<student_id>`** (`delete_student`): 
            Instancia um objeto temporário (placeholder) do estudante com o ID fornecido para executar 
            a sua remoção da base de dados através do serviço correspondente.
            
        4.  **POST `/students/edit/<student_id>`** (`edit_student`): 
            Coleta as propriedades atualizadas enviadas pelo formulário e aciona o serviço de atualização 
            para persistir as modificações dos dados cadastrais do estudante.
            
        5.  **GET `/students/<student_id>/courses`** (`view_student_courses`): 
            Monta uma representação simplificada do estudante para recuperar sua entidade completa via ID, 
            renderizando a view de cursos vinculados (`student_courses.html`).
        """

        @self.app.route("/students", methods=["GET"])
        def view_students():
            students_list = self._student_getter.get_all_students()
            return render_template("students.html", students=students_list)

        @self.app.route("/students/add", methods=["POST"])
        def add_student():
            name = request.form.get("name")
            tax_id = request.form.get("student_tax_id")
            
            if name and tax_id:
                new_student = Student(name=name, student_tax_id=tax_id)
                self._student_adder.add_student(new_student)
                
            return redirect(url_for("view_students"))

        @self.app.route("/students/delete/<student_id>", methods=["POST"])
        def delete_student(student_id):
            student_to_delete = Student(name="Placeholder", student_tax_id="000.000.000-00", student_id=student_id)
            self._student_deletion.delete_student(student_to_delete)
            
            return redirect(url_for("view_students"))

        @self.app.route("/students/edit/<student_id>", methods=["POST"])
        def edit_student(student_id):
            name = request.form.get("name")
            tax_id = request.form.get("student_tax_id")
            student_to_edit = Student(name=name, student_tax_id=tax_id, student_id=student_id)
            self._student_updater.update_student(student_to_edit)

            return redirect(url_for("view_students"))

        @self.app.route("/students/<student_id>/courses", methods=["GET"])
        def view_student_courses(student_id):
            dumb_student = Student(name="PlaceHolder",student_tax_id="00000000000",student_id=student_id,courses=[])

            student = self._student_getter_by_id.get_student_by_id(dumb_student)

            # e renderizaria em uma página dedicada como 'student_courses.html'
            return render_template("student_courses.html", student=student)
Aqui está o código do seu arquivo de inicialização (`__main__.py`) com **docstrings completas e detalhadas** no padrão **Google Style** (o mais recomendado e legível para a comunidade Python).

---

```python
"""Módulo principal do aplicativo GPA Calculator.

Este módulo atua como o ponto de entrada (entry point) do sistema, realizando 
o bootstrap da aplicação. Ele configura as injeções de dependência entre a 
infraestrutura de persistência, os serviços de domínio de aplicação e a camada 
de apresentação baseada no Flask.
"""

import os
from flask import Flask, render_template

from src import (
    Context, 
    StudentRepository, 
    CourseRepository, 
    StudentAdderService, 
    StudentGetterService, 
    StudentGetterByIdService, 
    StudentDeletionService, 
    StudentUpdatableService,
    CourseGetterService,
    CourseAdderService,
    CourseUpdatableService,
    CourseDeletionService,
    HomeController,
    StudentController,
    CourseController
)


def bootstrap() -> None:
    """Inicializa, configura e executa o servidor web do GPA Calculator.

    Esta função executa o bootstrap do sistema, realizando as seguintes etapas:
        1. Configura os contextos de dados persistidos em arquivos CSV.
        2. Inicializa os repositórios (camada de infraestrutura).
        3. Instancia todos os casos de uso/serviços de aplicação para Alunos e Cursos.
        4. Define a pasta de templates e cria a instância da aplicação Flask.
        5. Injeta as dependências necessárias nos Controladores (Apresentação).
        6. Inicia o servidor de desenvolvimento do Flask.

    Returns:
        None
    """
    # 1. Inicialização do Contexto de Persistência (Infraestrutura)
    student_context = Context(file_name="student.csv")
    course_context = Context(file_name="course.csv")
    
    # 2. Inicialização do Repositório (Infraestrutura)
    student_repository = StudentRepository(context=student_context)
    course_repository = CourseRepository(context=course_context)
    
    # 3. Inicialização do Serviço (Aplicação)
    student_adder_service = StudentAdderService(student_repository=student_repository)
    student_deletion_service = StudentDeletionService(student_repository=student_repository, course_repository=course_repository)
    student_getter_service = StudentGetterService(student_repository=student_repository, course_repository=course_repository)
    student_getter_by_id_service = StudentGetterByIdService(student_repository=student_repository, course_repository=course_repository)
    student_updatable_service = StudentUpdatableService(student_repository=student_repository)
    
    # --- INSTANCIAÇÃO DOS CASOS DE USO DE CURSOS ---
    course_getter_service = CourseGetterService(course_repository=course_repository)
    course_adder_service = CourseAdderService(course_repository=course_repository, student_repository=student_repository)
    course_deletion_service = CourseDeletionService(course_repository=course_repository, student_repository=student_repository)
    course_updatable_service = CourseUpdatableService(course_repository=course_repository)

    # 4. Configuração da Apresentação Web (Flask)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_folder = os.path.join(current_dir, "src", "presentation", "web", "templates")
    
    app = Flask(__name__, template_folder=template_folder)

    # 5. Administração e Ativação dos Controllers (Com as novas dependências injetadas)
    HomeController(app=app)
    StudentController(
        app=app,
        student_getter=student_getter_service,
        student_getter_by_id=student_getter_by_id_service,
        student_adder=student_adder_service,
        student_deletion=student_deletion_service,
        student_updater=student_updatable_service
    )
    
    CourseController(
        app=app,
        courser_getter=course_getter_service,
        course_adder=course_adder_service,
        course_updatable=course_updatable_service,
        course_deletion=course_deletion_service,
    )

    # 6. Inicialização do Servidor
    print("\n🚀 Servidor do GPA Calculator rodando perfeitamente!")
    print("👉 Acesse a Home do sistema em: http://127.0.0.1:5000/\n")
    
    app.run(debug=True, port=5000)


if __name__ == "__main__":
    bootstrap()

from flask import Flask, request, render_template, redirect, url_for

from src.domain.entities.course import Course 

from src.application.services_contract.course_contract.course_adder_contract import CourseAdderContract
from src.application.services_contract.course_contract.course_getter_contract import CourseGetterContract
from src.application.services_contract.course_contract.course_updatable_contract import CourseUpdatableContract
from src.application.services_contract.course_contract.course_deletion_contract import CourseDeletionContract

class CourseController:
    def __init__(
            self,
            app: Flask,
            courser_getter: CourseGetterContract,
            course_adder: CourseAdderContract,
            course_updatable: CourseUpdatableContract,
            course_deletion: CourseDeletionContract
        ):
        self.app = app
        self._course_getter = courser_getter
        self._course_adder = course_adder
        self._course_updatable = course_updatable
        self._course_deletion = course_deletion
        
        self._register_routes()

    def _register_routes(self):
        
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
from flask import Flask, render_template, request, redirect, url_for

from src.domain.entities.student import Student
from src.application.services_contract.student_contract.student_getter_contract import StudentGetterContract
from src.application.services_contract.student_contract.student_getter_by_id_contract import StudentGetterByIdContract
from src.application.services_contract.student_contract.student_adder_contract import StudentAdderContract
from src.application.services_contract.student_contract.student_deletion_contract import StudentDeletionContract
from src.application.services_contract.student_contract.student_updatable_contract import StudentUpdatableContract

class StudentController:
    def __init__(
            self,
            app: Flask,
            student_getter:StudentGetterContract,
            student_getter_by_id:StudentGetterByIdContract,
            student_adder:StudentAdderContract,
            student_deletion:StudentDeletionContract,
            student_updater:StudentUpdatableContract
        ):
        self.app = app
        self._student_getter = student_getter
        self._student_getter_by_id = student_getter_by_id
        self._student_adder = student_adder
        self._student_deletion = student_deletion
        self._student_updater = student_updater
        self._register_routes()

    def _register_routes(self):

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
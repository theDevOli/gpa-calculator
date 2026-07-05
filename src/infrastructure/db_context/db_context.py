# from io import TextIOWrapper
# import os

# class Context:
#     _student_header = "student_id,name,student_tax_id,courses_id"
#     _course_header = "course_id,name,credit_hours,grade"
    
#     def __init__(self, file_name: str):
#         if not file_name:
#             raise ValueError("O nome do arquivo não pode ser vazio.")
#         if file_name != 'student.csv' and file_name != 'course.csv':
#             raise ValueError("O nome do arquivo deve ser 'student.csv' ou 'course.csv'.")
        
#         self.file_name = file_name

#         self.header = self._student_header if file_name == 'student.csv' else self._course_header
        
#         db_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "db"))
#         os.makedirs(db_dir, exist_ok=True)
        
#         self.path = os.path.join(db_dir, self.file_name)
        
#         if not os.path.exists(self.path) or os.path.getsize(self.path) == 0:
#             with open(self.path, 'w') as file:
#                 file.write(self.header)
    
#     def _reader(self) -> list:
#         if not os.path.exists(self.path):
#             return []
            
#         with open(self.path, 'r') as file:
#             lines = file.readlines()

#         return [line for line in lines[1:] if line.strip()]
    
#     def _appender(self, csv_data: str):
#         with open(self.path, 'a') as file:
#             file.write(f'\n{csv_data}')
    
#     def get_all_entities(self) -> list:
#         return self._reader()
    
#     def save_entity(self, csv_data: str):
#         self._appender(csv_data)
    
#     def update_entity(self, updated_csv_data: str, entity_id: str):
#             lines_without_header = self._reader()
            
#             with open(self.path, 'w') as file:
#                 file.write(f"{self.header}")

#                 for line in lines_without_header:
#                     if line.strip().startswith(entity_id):
#                         file.write(f'\n{updated_csv_data}')
#                     elif line.strip():
#                         file.write(line)
    
#     def remove_entity(self, entity_id: str):
#         lines_without_header = self._reader()
        
#         with open(self.path, 'w') as file:
#             file.write(f"{self.header}")

#             for line in lines_without_header:
#                 if not line.strip().startswith(entity_id) and line.strip():
#                     file.write(f'\n{line}')
import os

class Context:
    _student_header = "student_id,name,student_tax_id,courses_id"
    _course_header = "course_id,name,credit_hours,grade"

    def __init__(self, file_name: str):
        if not file_name:
            raise ValueError("O nome do arquivo não pode ser vazio.")

        if file_name not in ("student.csv", "course.csv"):
            raise ValueError(
                "O nome do arquivo deve ser 'student.csv' ou 'course.csv'."
            )

        self.file_name = file_name
        self.header = (
            self._student_header
            if file_name == "student.csv"
            else self._course_header
        )

        db_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "db")
        )
        os.makedirs(db_dir, exist_ok=True)

        self.path = os.path.join(db_dir, self.file_name)

        if not os.path.exists(self.path) or os.path.getsize(self.path) == 0:
            with open(self.path, "w", encoding="utf-8") as file:
                file.write(self.header)

    def _reader(self) -> list[str]:
        if not os.path.exists(self.path):
            return []

        with open(self.path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        return [
            line.strip()
            for line in lines[1:]
            if line.strip()
        ]

    def _appender(self, csv_data: str):
        with open(self.path, "a", encoding="utf-8") as file:
            if os.path.getsize(self.path) > len(self.header):
                file.write("\n")

            file.write(csv_data)

    def get_all_entities(self) -> list[str]:
        return self._reader()

    def save_entity(self, csv_data: str):
        self._appender(csv_data)

    def update_entity(self, updated_csv_data: str, entity_id: str):
        lines = self._reader()

        with open(self.path, "w", encoding="utf-8") as file:
            file.write(self.header)

            for line in lines:
                if line.startswith(entity_id):
                    file.write(f"\n{updated_csv_data}")
                else:
                    file.write(f"\n{line}")

    def remove_entity(self, entity_id: str):
        lines = self._reader()

        with open(self.path, "w", encoding="utf-8") as file:
            file.write(self.header)

            for line in lines:
                if not line.startswith(entity_id):
                    file.write(f"\n{line}")
import json
import os


class Student:
    def __init__(self, student_id, name, grade):
        self.student_id = student_id
        self.name = name
        self.grade = grade

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "grade": self.grade
        }

    def __str__(self):
        return f"ID: {self.student_id:<6} Name: {self.name:<20} Grade: {self.grade}"


class StudentManager:
    def __init__(self, filename="students.json"):
        self.filename = filename
        self.students = []
        self.load_from_file()

    def load_from_file(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.students = [Student(d["student_id"], d["name"], d["grade"]) for d in data]

    def save_to_file(self):
        data = [s.to_dict() for s in self.students]
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def find_student(self, student_id):
        for s in self.students:
            if s.student_id == student_id:
                return s
        return None

    def add_student(self, student_id, name, grade):
        if self.find_student(student_id) is not None:
            print(f"Error: A student with ID '{student_id}' already exists.")
            return False
        new_student = Student(student_id, name, grade)
        self.students.append(new_student)
        self.save_to_file()
        print(f"Student '{name}' added successfully.")
        return True

    def update_student(self, student_id, name=None, grade=None):
        student = self.find_student(student_id)
        if student is None:
            print(f"Error: No student found with ID '{student_id}'.")
            return False
        if name:
            student.name = name
        if grade:
            student.grade = grade
        self.save_to_file()
        print(f"Student '{student_id}' updated successfully.")
        return True

    def delete_student(self, student_id):
        student = self.find_student(student_id)
        if student is None:
            print(f"Error: No student found with ID '{student_id}'.")
            return False
        self.students.remove(student)
        self.save_to_file()
        print(f"Student '{student_id}' deleted successfully.")
        return True

    def list_students(self):
        if not self.students:
            print("No student records found.")
            return
        print("-" * 50)
        for s in self.students:
            print(s)
        print("-" * 50)


def main():
    manager = StudentManager()

    menu = """
====== Student Management System ======
1. Add Student
2. Update Student
3. Delete Student
4. List All Students
5. Exit
========================================
"""

    while True:
        print(menu)
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            student_id = input("Enter Student ID: ").strip()
            name = input("Enter Name: ").strip()
            grade = input("Enter Grade: ").strip()
            manager.add_student(student_id, name, grade)

        elif choice == "2":
            student_id = input("Enter Student ID to update: ").strip()
            name = input("Enter new Name (leave blank to skip): ").strip()
            grade = input("Enter new Grade (leave blank to skip): ").strip()
            manager.update_student(student_id, name or None, grade or None)

        elif choice == "3":
            student_id = input("Enter Student ID to delete: ").strip()
            manager.delete_student(student_id)

        elif choice == "4":
            manager.list_students()

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
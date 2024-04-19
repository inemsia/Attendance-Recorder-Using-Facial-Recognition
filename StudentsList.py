import os, sys
sys.path.append(os.getcwd())
from Student import Student

# This class contains and manipulates the list of students.
class StudentsList:

    # Constructor
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.list_of_students = []
        self.number_of_students = 0

    # Loads student data present in the directory
    def load(self):
        for student_name in os.listdir(self.folder_path):
            self.add_student(student_name)

    # Adds student folder to directory. Adds student name to the list.
    def add_student(self, student_name):
        student_path = self.folder_path + '/' + student_name
        added_student = Student(student_name, student_path)
        if self.find_student(student_name) == -1:
            self.list_of_students.append(added_student)
            self.number_of_students += 1
        if os.path.exists(student_path):
            print(f"{student_name}'s folder already exists")
        else:
            os.mkdir(student_path)

    # Removes all student information (name from list, pictures and folder from directory)
    def delete_student(self, name):
        if self.number_of_students == 0:
            return
        # Remove student from list
        position = self.find_student(name)
        if position == -1:
            print(f"Student {name} does not exist")
            return
        student = self.list_of_students.pop(position)
        self.number_of_students -= 1
        # Remove student folder and pictures
        student_path = self.path + "/" + student.get_name()
        # Remove images in student folder
        for image_name in os.listdir(student_path):
            image_path = student_path + "/" + image_name
            os.remove(image_path)
        # Delete student folder
        os.rmdir(student_path)

    # Finds student's position on the list
    def find_student(self, name):
        for i in range(len(self.list_of_students)):
            student = self.list_of_students[i]
            if student.get_name() == name:
                return i
        return -1

    # Uses find_student to get the Student object
    def get_student(self, name):
        position = self.find_student(name)
        return self.list_of_students[position]

    # Returns list_of_students
    def get_list_of_students(self):
        return self.list_of_students

    # Returns folder_path
    def get_path(self):
        return self.folder_path

    # Returns number_of_students
    def get_number_of_students(self):
        return self.number_of_students

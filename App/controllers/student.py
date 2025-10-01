from App.database import db
from App.models import Student

# STUDENT CONTROLLERS

def create_student(fullname,age,year):
    student = Student(fullname=fullname,age=age,year=year)
    db.session.add(student)
    db.session.commit()
    return student

def get_all_students():
    students = Student.query.all()
    return [s.to_json() for s in students]

def get_student(student_id):
    return Student.query.get(student_id)
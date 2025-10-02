from App.database import db
from App.models import Student, VolunteerRecord

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

def update_student_hours(student):
    total_hours = db.session.query(db.func.sum(VolunteerRecord.hours))\
       .filter_by(student_id=student.studentId, confirmed=True).scalar() or 0
    student.hours = total_hours
    db.session.commit()
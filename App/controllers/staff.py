from App.database import db
from App.models import Student, Staff, VolunteerRecord, Accolade, StudentAccolade, Leaderboard
from App.controllers.student import update_student_hours
from datetime import date

# STAFF CONTROLLERS
def create_staff(username, department, password):
    staff = Staff(username=username, department=department, password=password)
    db.session.add(staff)
    db.session.commit()
    return staff

def get_all_staff():
    staff = Staff.query.all()
    return [s.to_json() for s in staff]

def get_staff(staff_id):
    return Staff.query.get(staff_id)

def confirm_hours(volunteer_id, confirm=True):
    record = VolunteerRecord.query.get(volunteer_id)
    if not record:
        raise ValueError(f"No volunteer record with ID {volunteer_id}")
    record.confirmed = confirm
    db.session.commit()
    
    if confirm:
        student = record.student
        update_student_hours(student)
    return record

def log_hours(student_id, hours, staff_id, description=""):
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"No student found with ID {student_id}")
    record = VolunteerRecord(
        student_id=student_id,
        staff_id=staff_id,
        hours=hours,
        description=description,
        confirmed=False, 
        date=date.today(), 
        )
    db.session.add(record)
    db.session.commit()
    return record
from App.database import db
from App.models import Student, Staff, VolunteerRecord, Accolade, StudentAccolade, Leaderboard

# STAFF CONTROLLERS
def create_staff(username, department):
    staff = Staff(username=username, department=department)
    db.session.add(staff)
    db.session.commit()
    return staff

def get_all_staff():
    staff = Staff.query.all()
    return [s.to_json() for s in staff]

def get_staff(staff_id):
    return Staff.query.get(staff_id)
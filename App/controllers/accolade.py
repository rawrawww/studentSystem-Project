from App.database import db
from App.models import Student, Staff, VolunteerRecord, Accolade, StudentAccolade, Leaderboard

# ACCOLADES

def check_accolades(student):
    accolades = Accolade.query.all()
    for accolade in accolades:
        if student.hours >= accolade.threshold:
            # Check if student already has it
            existing = StudentAccolade.query.filter_by(studentId=student.id, accoladeId=accolade.id).first()
            if not existing:
                new_award = StudentAccolade(studentId=student.id, accoladeId=accolade.id)
                db.session.add(new_award)
                db.session.commit()
                print(f"🏅 Student {student.username} earned accolade: {accolade.title}")


def get_all_students_accolades():
    data = []
    students = Student.query.all()
    for s in students:
        accolades = StudentAccolade.query.filter_by(studentId=s.id).all()
        accolade_list = [Accolade.query.get(a.accoladeId).to_json() for a in accolades]
        data.append({"student": s.to_json(), "accolades": accolade_list})
    return data

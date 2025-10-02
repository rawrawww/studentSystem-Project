from App.database import db
from App.models import Student, VolunteerRecord, Accolade, StudentAccolade

# ACCOLADES

def check_accolades(student):

    update_student_hours(student)
    print(f"Checking accolades for student {student.fullname} with {student.hours} hours")

    accolades = Accolade.query.all()
    for accolade in accolades:
        print(f"Checking accolade {accolade.title} with threshold {accolade.threshold}")
        if student.hours >= accolade.threshold:
            # Check if student already has this accolade
            existing = StudentAccolade.query.filter_by(
                studentId=student.studentId,
                accoladeId=accolade.id
            ).first()
            if not existing:
                new_award = StudentAccolade(
                    studentId=student.studentId,
                    accoladeId=accolade.id
                )
                db.session.add(new_award)
                db.session.commit()
                print(f"Student {student.fullname} earned accolade: {accolade.title}")
            else:
                print(f"Student {student.fullname} already has accolade: {accolade.title}")
        else:
            print(f"Student {student.fullname} does not meet threshold for accolade: {accolade.title}")


def get_all_students_accolades():
    students = Student.query.all()
    data = []
    for s in students:
        # Make sure hours are updated
        update_student_hours(s)
        check_accolades(s)

        # Get all accolades for this student
        accolades = StudentAccolade.query.filter_by(studentId=s.studentId).all()
        accolade_list = [Accolade.query.get(a.accoladeId).to_json() for a in accolades]
        data.append({
            "student": s.to_json(),
            "accolades": accolade_list
        })
    return data


def update_student_hours(student):
   total_hours = db.session.query(db.func.sum(VolunteerRecord.hours))\
        .filter_by(student_id=student.studentId, confirmed=True).scalar() or 0
   student.hours = total_hours
   db.session.commit()


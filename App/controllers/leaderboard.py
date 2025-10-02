from App.database import db
from App.models import Student, VolunteerRecord

def get_leaderboard():
    results = db.session.query(
        Student.fullname,
        db.func.sum(VolunteerRecord.hours).label("total_hours")
    ).join(VolunteerRecord, VolunteerRecord.student_id == Student.studentId)\
     .group_by(Student.studentId).order_by(db.desc("total_hours")).all()

    return [{"student": r.fullname, "hours": r.total_hours} for r in results]
from App.database import db
from App.models import VolunteerRecord
from App.controllers.student import update_student_hours

def request_hours(student_id, hours, staff_id=None, description=""):
    """Create a new volunteer record request."""
    from datetime import date
    
    record = VolunteerRecord(
        student_id=student_id,
        staff_id=staff_id if staff_id else 1,
        date=date.today(),
        description=description,
        confirmed=False,
        hours=hours
    )
    db.session.add(record)
    db.session.commit()
    return record

def get_all_hours_requests():
    """Return all volunteer records (pending or confirmed)."""
    records = VolunteerRecord.query.all()
    return [r.get_json() for r in records]

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

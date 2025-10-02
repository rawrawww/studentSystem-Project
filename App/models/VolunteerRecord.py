from App.database import db

class VolunteerRecord(db.Model):
    volunteerId = db.Column(db.Integer, primary_key=True) 
    student_id= db.Column(db.Integer, db.ForeignKey('student.studentId'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staffId'), nullable=False)
    date= db.Column(db.Date, nullable=False)
    description = db.Column(db.String(100))
    confirmed = db.Column(db.Boolean, default=False)
    hours = db.Column(db.Float, nullable=False)  

    staff = db.relationship('Staff', back_populates='volunteer_logs')
    student = db.relationship('Student', back_populates='volunteer_logs')

    def get_json(self):
        return {
            'id': self.volunteerId,
            'student_id': self.student_id,
            'staff_id': self.staff_id,
            'hours': self.hours,
            'description': self.description,
            'confirmed': self.confirmed
        }
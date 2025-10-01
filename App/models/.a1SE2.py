from App.database import db
from .user import User

class Staff(User):
     __tablename__ = 'staff'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    department = db.Column(db.String(50))

    # relationship: staff can log hours for students
    volunteer_logs = db.relationship('VolunteerLog', backref='staff', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'staff',
    }

    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'department': self.department
        }


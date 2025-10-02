from App.database import db
from werkzeug.security import generate_password_hash, check_password_hash

class Student(db.Model):

    studentId = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    year= db.Column(db.String(10), nullable=False)
    hours = db.Column(db.Float, nullable=False, default=0)
    

    # relationships
    volunteer_logs = db.relationship('VolunteerRecord', back_populates='student', lazy=True)
    accolades = db.relationship('StudentAccolade', back_populates='student')

    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

    def __init__(self, fullname, age, year):
        self.fullname = fullname
        self.age = age
        self.year=year
        
    def set_password(self, password):
        
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
       
        return check_password_hash(self.password, password)
    
    def to_json(self):
        return {
            "studentId": self.studentId,
            "fullname": self.fullname,
            "age": self.age,
            "year": self.year,
            "hours": self.hours
        }




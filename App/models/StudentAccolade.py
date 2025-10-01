from App.database import db

class StudentAccolade(db.Model):
    __tablename__ = 'student_accolade'
    id = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.Integer, db.ForeignKey('student.studentId'), nullable=False)
    accoladeId = db.Column(db.Integer, db.ForeignKey('accolade.id'), nullable=False)

    student = db.relationship('Student', back_populates='accolades')
    accolade = db.relationship('Accolade', back_populates='students')

   

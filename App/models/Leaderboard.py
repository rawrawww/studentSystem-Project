from App.database import db

class Leaderboard(db.Model):
    __tablename__ = "leaderboard"
    id = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.Integer, db.ForeignKey("student.studentId"))
    total_hours = db.Column(db.Float)


from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class Staff(db.Model):
   
    staffId = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(50))

    # relationship: staff can log hours for students
    volunteer_logs = db.relationship('VolunteerRecord', back_populates='staff', lazy=True)

    def __init__(self, department):
      self.department = department


    def set_password(self, password):
      """Create hashed password."""
      self.password = generate_password_hash(password)
    
    def check_password(self, password):
      """Check hashed password."""
      return check_password_hash(self.password, password)



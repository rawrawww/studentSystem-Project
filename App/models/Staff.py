from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class Staff(db.Model):
   
    staffId = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(50))
    username= db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
       
    volunteer_logs = db.relationship('VolunteerRecord', back_populates='staff', lazy=True)

    def __init__(self, username, department, password):
        self.username = username
        self.department = department
        self.set_password(password)


    def set_password(self, password):
     
      self.password = generate_password_hash(password)
    
    def check_password(self, password):
      
      return check_password_hash(self.password, password)
    
    def to_json(self):
        return {
            "id": self.staffId,
            "username": self.username,
            "department": self.department
        }



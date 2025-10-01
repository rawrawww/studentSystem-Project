from App.database import db

class Accolade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    threshold= db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200))

    students = db.relationship('StudentAccolade', back_populates='accolade')

    def __init__(self, title, threshold, description=""):
        self.title = title
        self.threshold=threshold
        self.description = description

   

    
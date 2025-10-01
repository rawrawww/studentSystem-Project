from App.database import db
from App.models import Leaderboard

def get_leaderboard():
    return db.session.scalars(db.select(Leaderboard)).all()
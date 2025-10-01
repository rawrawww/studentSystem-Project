from App.database import db

class Leaderboard:
    
    @staticmethod
    def get_leaderboard():
        results = db.session.query(
            Student.username,
            db.func.sum(VolunteerLog.hours).label("total_hours")
        ).join(VolunteerLog).group_by(Student.id).order_by(db.desc("total_hours")).all()

        return [{"student": r.username, "hours": r.total_hours} for r in results]
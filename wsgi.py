import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import (Student, Staff, VolunteerRecord, Accolade, StudentAccolade, Leaderboard)
from App.main import create_app
from App.controllers import (
    create_student,
    get_all_students, 
    get_all_students_accolades, 
    get_leaderboard,
    request_hours, 
    get_all_hours_requests, 
    confirm_hours,
    initialize
)
from App.models.Leaderboard import Leaderboard
from App.controllers.staff import create_staff, get_all_staff, confirm_hours
from App.controllers.staff import log_hours 

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    
    accoladeTenHours=Accolade(title="10 Hours", threshold=10, description="Awarded a bronze badge for completing 10 volunteer hours")
    accoladeTwentyHours=Accolade(title="20 Hours", threshold=20, description="Awarded a silver badge for completing 20 volunteer hours")
    accoladeFiftyHours=Accolade(title="50 Hours", threshold=50, description="Awarded a gold badge for completing 50 volunteer hours")

    db.session.add(accoladeTenHours)
    db.session.add(accoladeTwentyHours)
    db.session.add(accoladeFiftyHours)
    db.session.commit()

    print('database intialized')

'''
Student Commands
'''

# Student Account Commands
student_cli = AppGroup('student', help='Create Student object commands')
@student_cli.command("create", help="create students in the database")
@click.argument("fullname", nargs=-1)
@click.argument("age", type=int)
@click.argument("year", type=str)

def create_student_command(fullname,age,year):
    fullname_str = " ".join(fullname) 
    student= create_student(fullname=fullname_str,age=age,year=year)
    print(f'Student {student.fullname} created with id {student.studentId}')
    print(get_all_students())

#Student Acolades
@student_cli.command("accolades", help="Show Accolades students")
def student_accolades_command():
    print(get_all_students_accolades())

#Student LeaderBoard
@student_cli.command("leaderboard", help="Show Leaderboard")
def student_leaderboard_command():
    data = get_all_students_accolades()
    if not data:
        print("No students found.")
        return
    
    for entry in data:
        student = entry["student"]
        accolades = entry["accolades"]
        print(f"Student: {student['fullname']} (ID: {student['studentId']}, Age: {student['age']}, Year: {student['year']}, Total Hours: {student['hours']})")
        
        if accolades:
            print("  Earned Accolades:")
            for accolade in accolades:
                print(f"    - {accolade['title']} (Threshold: {accolade['threshold']} hours) - {accolade['description']}")
        else:
            print(" No accolades earned yet.")
        
        print()  
  

#Student Hours
@student_cli.command("request", help="Reqest Hours")
@click.argument("studentid", type=int)
@click.argument("hours", type=int)
def student_request_command(studentid, hours):
    request_hours(studentid, hours)
    print(f'Student {studentid} requested {hours} hours')
app.cli.add_command(student_cli) # add the group to the cli

'''
Staff Commands
'''

# Staff Account Commands
staff_cli = AppGroup('staff', help='Staff object commands')
@staff_cli.command("create", help="creat staff in the database")
@click.argument("department", type=str)
@click.argument("username", type=str)
@click.argument("password", type=str)
def create_staff_command(username, department, password):
    staff= create_staff(username=username, department=department, password=password)
    staffId= staff.staffId
    print(f'Staff {staff.department} created with id {staff.staffId}')
    print(get_all_staff())

#Staff Record Hours
staff_cli.command("Record", help="Record Hours for a student")
@click.argument("staffId", type=int)
@click.argument("status", type=bool)
def staff_record_command(staffId,volunteerId,status):
    if status:
        confirm_hours(volunteerId, confirm=True)
        print(f'CONFIRMED volunteer record {volunteerId}')
    else:
        confirm_hours(volunteerId, confirm=False)
        print(f'DENIED volunteer record {volunteerId}')

#Staff View Requests
@staff_cli.command("view", help="View all volunteer records")
def view_volunteer_records():
    records = VolunteerRecord.query.all()
    for r in records:
        print({
            "volunteerId": r.volunteerId,
            "student_id": r.student_id,
            "hours": r.hours,
            "confirmed": r.confirmed,
            "description": r.description
        })

app.cli.add_command(staff_cli)


#Staff Confirm Hours
@staff_cli.command("confirm", help="Confirm volunteer hours")
@click.argument("volunteer_record_id", type=int)
@click.argument("confirm", type=bool, default=True)
def confirm_hours_command(volunteer_record_id, confirm=True):
    record = confirm_hours(volunteer_record_id, confirm)
    print(f"Volunteer record {volunteer_record_id} confirmed: {confirm}")

#Staff Log Hours
@staff_cli.command("log", help="Log volunteer hours for a student")
@click.argument("staff_id", type=int)
@click.argument("student_id", type=int)
@click.argument("hours", type=float)
@click.argument("description", nargs=-1)
def log_hours_command(staff_id,student_id,hours, description):
    description_str = " ".join(description) 
    try:
        record = log_hours(student_id, hours, staff_id,description_str)
        print(f"Logged {hours} hours for student ID {student_id}. Record ID: {record.volunteerId}")
    except ValueError as e:
        print(str(e))

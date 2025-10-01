import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import (Student, Staff, VolunteerRecord, Accolade, StudentAccolade, Leaderboard)
from App.main import create_app
from App.controllers import ( create_student, create_staff, get_all_students, get_all_staff, get_all_students_accolades, get_leaderboard,
    request_hours, get_all_hours_requests, confirm_hours,initialize )


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
    print(get_leaderboard())   

#Student Hours
@student_cli.command("request", help="Reqest Hours")
@click.argument("studentId", type=int)
@click.argument("hours", type=int)
def student_request_command(studentId, hours):
    request_hours(studentId, hours)
    print(f'Student {studentId} requested {hours} hours')
app.cli.add_command(student_cli) # add the group to the cli

'''
Staff Commands
'''

# Staff Account Commands
staff_cli = AppGroup('staff', help='Staff object commands')
@staff_cli.command("create", help="creat staff in the database")
@click.argument("username", type=str)
def create_staff_command(username):
    staff= create_staff(username)
    staffId= staff.staffId
    print(f'Staff {staff.username} created with id {staff.id}')
    print(get_all_staff())

#Staff Record Hours
staff_cli.command("Record", help="Record Hours for a student")
@click.argument("staffId", type=int)
@click.argument("houstatus", type=int)
def staff_record_command(staffId, hours):
    if(status==True):
        print(f'CONFIRMED)')
    elif (status==False):
        print(f'DENIED')   
    else:
        print(f'INVALID STATUS')

#Staff View Requests
@staff_cli.command("view", help="View Hours Requests")
@click.argument("volunteerId", type=int)
def staff_view_command():
    print(get_all_hours_requests())

#Staff Confirm Hours
@staff_cli.command("confirm", help="Confirm Hours for a student")
@click.argument("volunteerId", type=int)
def staff_confirm_command(volunteerId):
    confirm_hours(volunteerId)
    print(f'Staff confirmed hours for volunteer record {volunteerId}')

app.cli.add_command(staff_cli) # add the group to the cli
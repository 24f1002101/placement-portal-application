from main import app 
from celery import Celery
import time
from model.models import *
from controllers.user_datastore import user_datastore
from celery.schedules import crontab
from mail import send_email
from datetime import datetime
from datetime import timedelta
from datetime import date,timedelta

from sqlalchemy import func
celery = Celery(
    'tasks',
    broker = 'redis://localhost:6379/0'
)
celery.conf.update(
    timezone = 'Asia/Kolkata',
    enable_utc = False
)
celery.conf.beat_schedule = {
    'send-deadline-reminders': {
        'task': 'celery_app.send_deadline_reminders',
        'schedule': crontab(hour=23, minute=6),        
    },
    'send-email-admin-placements' : {
        'task' : 'celery_app.send_monthly_report',
        'schedule' : crontab(hour=16,minute=46),
    }
}

@celery.task()
def generate_csv(student_id):
    with app.app_context():
        applications = db.session.query(Application).filter(Application.student_id == student_id).all()
        #student_email = db.session.query(Student).filter(id==student_id).first().user.email
        data = []
        for i in applications:
            company = db.session.query(Company).filter(Company.id==i.drive.company_id).first()
            data.append({
                "id":i.student_id,
                "name" :i.student.user.name,
                "company_name" : company.company_name,
                "job_title":i.drive.job_title,
                "application_end_date":i.drive.application_deadline,
                "application_status":i.drive.status
            })
        csv_data = "id,name,company_name,job_title,application_end_date,application_status\n"
        for i in data:
            csv_data += str(i['id'])+","+i['name']+","+i['company_name']+","+i['job_title']+','+str(i['application_end_date'])+","+i['application_status']+"\n"
        file_written = open('history.csv','w')
        file_written.write(csv_data)
        print("CSV File Has Generated Successfully !!!")
        return 
        #send_email(student_email, 'CSV Generation Complete', 'The CSV file has been generated successfully.')


@celery.task()
def send_deadline_reminders():
    with app.app_context():
        today = datetime.now()
        deadline_limit = today + timedelta(days=10)  
        upcoming_drives = db.session.query(PlacementDrive).filter(
            PlacementDrive.status == 'approved',
            PlacementDrive.application_deadline >= today,
            PlacementDrive.application_deadline <= deadline_limit
        ).all()

        if not upcoming_drives:
            print("No upcoming deadlines")
            return

        users = db.session.query(User).all()

        for user in users:
            if not user.student_profile:
                continue

            student = user.student_profile
            # filter eligible upcoming drives in Python
            if student.status != 'approved':
                continue 

            eligible_upcoming = [
                drive for drive in upcoming_drives
                if (
                    student.branch.lower() in drive.eligibility_branch.lower() and
                    student.cgpa >= drive.eligibility_cgpa and
                    student.year == drive.eligibility_year 
                )
            ]

            # only remind about drives not yet applied to
            applied_drive_ids = [
                a.drive_id for a in db.session.query(Application).filter(
                    Application.student_id == student.id
                ).all()
            ]

            to_remind = [
                drive for drive in eligible_upcoming
                if drive.id not in applied_drive_ids
            ]

            if to_remind:
                drive_rows = "".join([
                    f"""
                    <tr>
                        <td>{d.job_title}</td>
                        <td>{d.company.company_name}</td>
                        <td style="color:red;">{d.application_deadline.strftime("%d %B %Y")}</td>
                    </tr>
                    """
                    for d in to_remind
                ])
                body = f"""
                <html>
                <body style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2>⏰ Deadline Reminder, {user.name}!</h2>
                    <p>The following drives are closing</p>
                    <table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse; width:100%;">
                        <thead style="background-color:#2980b9; color:white;">
                            <tr>
                                <th>Job Title</th>
                                <th>Company</th>
                                <th>Deadline</th>
                            </tr>
                        </thead>
                        <tbody>{drive_rows}</tbody>
                    </table>
                    <p>Login to the portal and apply before it's too late!</p>
                </body>
                </html>
                """
                send_email(user.email, "⏰ Upcoming Placement Deadlines - Apply Now!", body)
                print(f"Reminder sent to {user.email}")


@celery.task()
def send_monthly_report():
    with app.app_context():
        today = date.today()
        next_month = date.today() + timedelta(days=30)
        month_name = today.strftime("%B %Y")

        # same logic as your get_all_applications_ route
        drives_conducted = db.session.query(PlacementDrive).filter(
            func.date(PlacementDrive.application_deadline) <= next_month
        ).all()

        total_drives = len(drives_conducted)
        total_applied_all = 0
        total_selected_all = 0
        drive_rows = ""

        for drive in drives_conducted:
            applications = db.session.query(Application).filter(
                Application.drive_id == drive.id
            ).all()
            total_applied = len(applications)
            total_selected = len([a for a in applications if a.status == 'selected'])
            total_applied_all += total_applied
            total_selected_all += total_selected
            company = db.session.query(Company).filter(Company.id == drive.company_id).first()

            drive_rows += f"""
            <tr>
                <td>{drive.id}</td>
                <td>{company.company_name}</td>
                <td>{drive.job_title}</td>
                <td>{total_applied}</td>
                <td>{total_selected}</td>
            </tr>
            """

        html = f"""
        <!DOCTYPE html>
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2>Monthly Placement Report - {month_name}</h2>
            <p>Generated on: {today.strftime("%d %B %Y")}</p>

            <h3>Summary</h3>
            <table border="1" cellpadding="8" cellspacing="0">
                <tr>
                    <th>Total Drives</th>
                    <th>Total Applied</th>
                    <th>Total Selected</th>
                </tr>
                <tr>
                    <td>{total_drives}</td>
                    <td>{total_applied_all}</td>
                    <td>{total_selected_all}</td>
                </tr>
            </table>

            <h3>Drive-wise Breakdown</h3>
            <table border="1" cellpadding="8" cellspacing="0">
                <thead>
                    <tr>
                        <th>Drive ID</th>
                        <th>Company</th>
                        <th>Job Role</th>
                        <th>Applied</th>
                        <th>Selected</th>
                    </tr>
                </thead>
                <tbody>
                    {drive_rows if drive_rows else '<tr><td colspan="5">No drives this month</td></tr>'}
                </tbody>
            </table>

            <p style="color: grey; font-size: 12px;">
                This is an automated report from the Placement Portal.
            </p>
        </body>
        </html>
        """

        admin = user_datastore.find_user(email='alambalaji1972@gmail.com')
        if admin:
            send_email(
                to_email=admin.email,
                subject=f"Monthly Placement Report - {month_name}",
                body=html
            )
            print(f"Monthly report sent to {admin.email}")
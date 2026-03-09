from main import app 
from flask import jsonify , make_response , request
from model.models import *
from flask_security import roles_required , auth_required
from controllers.user_datastore import user_datastore
from datetime import datetime,date
today = date.today()
from sqlalchemy import func
from sqlalchemy import or_
@app.route('/api/create_drive',methods=['POST'])
@auth_required('token')
@roles_required('company')
def create_drive():
    data = request.get_json()
    eligible_year = int(data.get('eligible_year'))
    eligible_branch = data.get('eligible_branch')
    cgpa = float(data.get('cutoff_cgpa'))
    email = data.get('email')
    application_deadline = data.get('application_deadline')
    application_deadline_obj = None
    job_name = data.get('job_role')
    job_description = data.get('job_description')

    user_found = user_datastore.find_user(email=email)
    if(not user_found):
        output = {
            "message" : "User not Found !!!"
        }
        return make_response(jsonify(output),404)
    company_id = user_found.company_profile.id

    try :
        application_deadline_obj = datetime.strptime(application_deadline,'%Y-%m-%d')
    except ValueError:
        return make_response(jsonify({
            "message" : "Invalid Date Format !!!"
        }),400)
    new_drive = PlacementDrive(
        company_id = company_id,
        job_title = job_name,
        job_description = job_description,
        eligibility_branch = eligible_branch,
        eligibility_cgpa = cgpa,
        eligibility_year = eligible_year,
        application_deadline = application_deadline_obj,
        status = 'approved'
    )
    db.session.add(new_drive)
    db.session.commit()
    output = {
        "message" : "Successfully created the drive !!!"
    }
    return make_response(jsonify(output),200)    

@app.route('/api/ongoing_drives',methods=['POST'])
@auth_required('token')
@roles_required('company')
def ongoing_drives():
    data = request.get_json()
    email = data.get('email')
    if(not email):
        data = {
            "message" : "email required !!!"
        }
        return make_response(jsonify(data),400)
    user_found = user_datastore.find_user(email=email)
    if(user_found.company_profile):
        ongoing_drives = db.session.query(PlacementDrive).filter(PlacementDrive.status == 'approved',PlacementDrive.company_id==user_found.company_profile.id,func.date(PlacementDrive.application_deadline) >= today).all()
        result = []
        for i in ongoing_drives:
            company_related = db.session.query(Company).filter(Company.id == i.company_id).first()
            result.append(
                {
                    "id" : i.id,
                    "company_details" : {
                        "company_id" : company_related.id,
                        "company_name" : company_related.company_name,
                        "hr_contact" : company_related.hr_contact,
                        "website" : company_related.website,
                        "approval_status" : company_related.approval_status
                    },
                    "job_title" : i.job_title,
                    "job_description" : i.job_description,
                    "eligibility_branch" : i.eligibility_branch,
                    "eligibility_cgpa" : i.eligibility_cgpa,
                    "eligibility_year" : i.eligibility_year,
                    "application_deadline" : i.application_deadline,
                    "status"  : i.status
                }
            )
        return make_response(jsonify(result),200)
    return make_response(jsonify({
        "message" : "You are not a company to view your drives !!!"
    }),400)

@app.route('/api/closed_drives',methods=['POST'])
@auth_required('token')
@roles_required('company')
def closed_drives():
    data = request.get_json()
    email = data.get('email')
    if(not email):
        output = {
            "message" : "Email required !!!"
        }
        return make_response(jsonify(output),400)
    user_found = user_datastore.find_user(email = email)
    if(not user_found):
        ouput = {
            "message" : "User not found !!!"
        }
        return make_response(jsonify(output),404)
    if(user_found.company_profile):
        closed_drives = db.session.query(PlacementDrive).filter(PlacementDrive.company_id == user_found.company_profile.id,or_(PlacementDrive.status == 'closed',func.date(PlacementDrive.application_deadline) < today)).all()
        result = []
        for i in closed_drives:
            company_related = db.session.query(Company).filter(Company.id == i.company_id).first()
            result.append(
                {
                    "id" : i.id,
                    "company_details" : {
                        "company_id" : company_related.id,
                        "company_name" : company_related.company_name,
                        "hr_contact" : company_related.hr_contact,
                        "website" : company_related.website,
                        "approval_status" : company_related.approval_status
                    },
                    "job_title" : i.job_title,
                    "job_description" : i.job_description,
                    "eligibility_branch" : i.eligibility_branch,
                    "eligibility_cgpa" : i.eligibility_cgpa,
                    "eligibility_year" : i.eligibility_year,
                    "application_deadline" : i.application_deadline,
                    "status"  : i.status
                }
            )
        return make_response(jsonify(result),200)
    return make_response(jsonify({
        "message" : "You are not a company to view your drives !!!"
    }),400)
    
@app.route('/api/close_drive',methods=['PUT'])
@auth_required('token')
@roles_required('company')
def close_drive():
    data = request.get_json()
    placement_id = int(data.get('id'))
    if(not placement_id):
        output = {
            "message" : "required placement id to update !!!"
        }
        return make_response(jsonify(output),404)
    placement = db.session.query(PlacementDrive).filter(PlacementDrive.id == placement_id).first()
    if(not placement):
        output = {
            "message" : "placement drive with entered id is not found !!!"
        }
        return make_response(jsonify(output),404)
    placement.status = 'closed'
    db.session.commit()
    output = {
        "message" : "Successfully closed the drive with id " + str(placement_id) + "!!!"
    }
    return make_response(jsonify(output),200)

@app.route('/api/get_student_applications',methods=['POST'])
@auth_required('token')
@roles_required('company')
def get_student_applications():
    data = request.get_json()
    drive_id = int(data.get('drive_id'))
    if(not drive_id):
        output = {
            "message" : "drive id is required !!!"
        }
        return make_response(jsonify(output),400)
    
    drive_applications = db.session.query(Application).filter(Application.drive_id==drive_id,Application.status=='pending').all()
    result = []
    for i in drive_applications:
        result.append(
            {
                "student_name" : i.student.user.name,
                "student_id" : i.student_id
            }
        )
    return make_response(jsonify(result),200)

@app.route('/api/get_student_application_details',methods=['POST'])
@auth_required('token')
@roles_required('company')
def get_student_application_details():
    data = request.get_json()
    if(not data):
        output = {
            "message" : "data is required !!!"
        }
        return make_response(jsonify(output),400)
    drive_id = int(data.get('drive_id'))
    student_id = int(data.get('student_id'))
    if(not drive_id or not student_id):
        output = {
            "message" : "required drive id and student id !!!"
        }
        return make_response(jsonify(output),400)
    
    student_application = db.session.query(Application).filter(Application.drive_id==drive_id,Application.student_id==student_id).first()
    if(not student_application):
        output = {
            "message" : "student application not found !!!"
        }
        return make_response(jsonify(output),404)
    
    output = {
        "student_name" : student_application.student.user.name,
        "cgpa" : student_application.student.cgpa,
        "year" : student_application.student.year,
        "branch" : student_application.student.branch,
        "job_role" : student_application.drive.job_title,
        "student_id" : student_application.student_id,
        "drive_id" : student_application.drive_id
    }
    return make_response(jsonify(output),200)

@app.route('/api/change_details_application',methods=['PUT'])
@auth_required('token')
@roles_required('company')
def change_details_application():
    data = request.get_json()
    if(not data):
        output = {
            "message" : "Data is required !!!"
        }
        return make_response(jsonify(output),400)
    student_id = int(data.get('student_id'))
    drive_id = int(data.get('drive_id'))
    selected_value = data.get('value')
    if(not student_id or not drive_id or not selected_value):
        output = {
            "message" : "check the passing values !!!"
        }
        return make_response(jsonify(output),400)
    application_to_change = db.session.query(Application).filter(Application.student_id==student_id,Application.drive_id==drive_id).first()
    if(not application_to_change):
        output = {
            "message" : "application with student_id and drive_id is not present !!!"
        }
        return make_response(jsonify(output),404)
    
    application_to_change.status = selected_value
    db.session.commit()
    output = {
        "message" : "successfully changed the details of the application !!!"
    }
    return make_response(jsonify(output),200)
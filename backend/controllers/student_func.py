from flask import request,make_response,jsonify
from controllers.user_datastore import user_datastore
from model.models import *
from main import app
from flask_security import auth_required , roles_required , roles_accepted
import os
from flask import send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime,date
from sqlalchemy import func
UPLOAD_FOLDER = 'uploads/resumes'
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/edit_profile_student',methods=['POST'])
@auth_required('token')
@roles_required('student')
def edit_student_profile():
    data = request.get_json()
    name = data.get('name')
    email_to_change = data.get('changing_email')
    branch = data.get('branch')
    cgpa = data.get('cgpa')
    year = data.get('year')
    original_email = data.get('original_email')
    user_found = user_datastore.find_user(email = original_email)
    if(user_found):
        if(name):
            user_found.name = name
        user_found_email = user_datastore.find_user(email=email_to_change)
        if(user_found_email):
            output = {
                "message" : "Use Different Email , Email Already Taken !!!"
            }
            return make_response(jsonify(output),400)
        user_found.email = email_to_change
        if(branch):
            user_found.student_profile.branch = branch.lower()
        if(cgpa):
            user_found.student_profile.cgpa = float(cgpa)
        if(year):
            user_found.student_profile.year = int(year)
        db.session.commit()
        output = {
            "message" : "successfully updated details !!!",
            "email" : email_to_change,
            "name" : name,
            "year" : year,
            "cgpa" : cgpa,
            "branch" : branch,
            "status" : user_found.student_profile.status
        }
        return make_response(jsonify(output),200)
    output = {
        "message" : "User not found with the email !!!"
    }
    return make_response(jsonify(output),404)

@app.route('/api/display_all_approved_companies',methods=['GET'])
@auth_required('token')
@roles_required('student')
def display_companies_approved():
    approved = db.session.query(Company).filter(Company.approval_status=='approved').all()
    result=[]
    for i in approved:
        result.append({
            "company_id" : i.id,
            "company_name" : i.company_name
        })
    return make_response(
        jsonify(result),200
    )

@app.route('/api/display_necessary_information',methods=['POST'])
@auth_required('token')
@roles_required('student')
def necessary_information():
    data = request.get_json()
    email = data.get('email')
    user_found = user_datastore.find_user(email=email)
    if(user_found):
        name = user_found.name
        email = user_found.email
        branch = user_found.student_profile.branch
        cgpa = user_found.student_profile.cgpa
        year = user_found.student_profile.year
        output = {
            "name" : name,
            "email" : email,
            "branch" : branch,
            "cgpa" : cgpa,
            "year" : year
        }
        return make_response(jsonify(output),200)
    output = {
        "message" : "User Not Found with Given Email !!!"
    }
    return make_response(jsonify(output),404)

@app.route('/api/get_company_drives',methods=['POST'])
@auth_required('token')
@roles_required('student')
def get_company_drives():
    today = date.today()
    data = request.get_json()
    company_id = int(data.get('company_id'))
    email = data.get('email')
    user_found = user_datastore.find_user(email=email)
    print
    if(company_id):
        company_drives = db.session.query(PlacementDrive).filter(PlacementDrive.company_id == company_id,PlacementDrive.status=='approved',func.date(PlacementDrive.application_deadline) >= today).all()
        result = []
        for i in company_drives:
            if((user_found.student_profile.branch.lower() in i.eligibility_branch.lower()) and (user_found.student_profile.cgpa>=i.eligibility_cgpa) and (i.eligibility_year==user_found.student_profile.year)):
                result.append({
                    "placement_id" : i.id,
                    "job_title" : i.job_title,
                    "job_description" : i.job_description,
                    "eligibility_year" : i.eligibility_year,
                    "eligibility_branch" : i.eligibility_branch,
                    "eligibility_cgpa" : i.eligibility_cgpa,
                    "application_deadline" : i.application_deadline,
                })
        return make_response(jsonify(result),200)
    output = {
        "message" : "check company id !!!"
    }
    return make_response(jsonify(output),400)

@app.route('/api/apply_drive',methods=['POST'])
@auth_required('token')
@roles_required('student')
def apply_drive():
    resume =  request.files.get('resume')
    email = request.form.get('email')
    print(int(request.form.get('placement_id')))
    drive_id = int(request.form.get('placement_id'))

    if(not resume or not email or not drive_id):
        output = {
            "message" : "Check essential requirements !!!"
        }
        return make_response(jsonify(output),400)
    
    if(not allowed_file(resume.filename)):
        output = {
            "message" : "You are allowed to upload only PDF Format File !!!"
        }
        return make_response(jsonify(output),400)
    
    user_found = user_datastore.find_user(email=email)

    if(not user_found):
        output = {
            "message" : "User not found with the email !!!"
        }
        return make_response(jsonify(output),404)

    if(not user_found.student_profile):
        output = {
            "message" : "you are not student to apply for the drive !!!"
        }
        return make_response(jsonify(output),404)

    already_applied = db.session.query(Application).filter(Application.student_id == user_found.student_profile.id , Application.drive_id == drive_id).first()
    if(already_applied):
        output = {
            "message" : "You have already applied to this drive , please wait !!!"
        }
        return make_response(jsonify(output),400)
    
    filename = secure_filename(f"{user_found.student_profile.id}_{drive_id}_{resume.filename}")
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    resume.save(filepath)

    new_application = Application(
        student_id = user_found.student_profile.id,
        drive_id = drive_id,
        application_date = datetime.now(),
        status = 'pending',
        resume_path = filepath
    )
    db.session.add(new_application)
    db.session.commit()
    output = {
        "message" : "Applied for the role successfully !!!"
    }
    return make_response(jsonify(output),200)

@app.route('/api/get_history',methods=['POST'])
@auth_required('token')
@roles_required('student')
def get_history():
    data = request.get_json()
    email = data.get('email')
    user_found = user_datastore.find_user(email=email)
    if(not user_found):
        output = {
            "message" : "User not found !!!"
        }
        return make_response(jsonify(output),404)
    if(not user_found.student_profile):
        output = {
            "message" : "student profile with entered email doesnot exist !!!"
        }
        return make_response(jsonify(output),400)
    
    applications = db.session.query(Application).filter(Application.student_id==user_found.student_profile.id).all()
    history = []
    for i in applications:
        company = db.session.query(Company).filter(Company.id == i.drive.company_id).first()
        history.append({
            "application_id" : i.id,
            "job_role" : i.drive.job_title,
            "company_name" : company.company_name,
            "status" : i.status
        })
    result = {
        "student_id" : user_found.student_profile.id,
        "history" :history
    }
    print(result)
    return make_response(jsonify(result),200)

@app.route('/api/view_resume',methods=['POST'])
@auth_required('token')
@roles_accepted('company','admin')
def view_resume():
    data = request.get_json()
    if(not data):
        output = {
            "message" : "Required Data to view resume !!!"
        }
        return make_response(jsonify(output),400)
    student_id = int(data.get('student_id'))
    drive_id = int(data.get('drive_id'))
    if(not student_id or not drive_id):
        output = {
            "message" : "Required student_id and drive_id to retrieve application !!!"
        }
        return make_response(jsonify(output),400)
    
    application = db.session.query(Application).filter(Application.student_id==student_id,Application.drive_id==drive_id).first()
    if(not application):
        output = {
            "message" : "Application not found with entered student_id and drive_id !!!" 
        }
        return make_response(jsonify(output),404)
    
    directory = os.path.abspath(UPLOAD_FOLDER)
    filename = os.path.basename(application.resume_path)
    return send_from_directory(directory,filename)

@app.route('/api/get_csv',methods=['POST'])
@auth_required('token')
@roles_required('student')
def csv_generation():
    data = request.get_json()
    if(not data):
        output = {
            "message" : "Data is necessary to do work !!!"
        }
        return make_response(jsonify(output),400)
    student_id = int(data.get('student_id'))
    if(not student_id):
        output = {
            "message" : "student id required !!!"
        }
        return make_response(jsonify(output),400)
    student = db.session.query(Student).filter(Student.id==student_id).first()
    if(not student):
        output = {
            "message" : "Student not found with entered student_id !!!"
        }
        return make_response(jsonify(output),404)
    from celery_app import generate_csv
    generate_csv.delay(student_id)
    output = {
        "message" : "Successfully generated the CSV !!!"
    }
    return make_response(jsonify(output),200)


@app.route('/api/get_all_applications_',methods=['GET'])
def get_all_applications_():
    today = date.today()
    drives_conducted = db.session.query(PlacementDrive).filter(func.date(PlacementDrive.application_deadline)<=today).all()
    result = []
    for i in drives_conducted:
        applications = db.session.query(Application).filter(Application.drive_id==i.id,func.date(Application.application_date)<=today).all()
        total_selected = len([i for i in applications if(i.status == 'selected')])
        total_applied = len([i for i in applications])
        company = db.session.query(Company).filter(Company.id==i.company_id).first()
        result.append({
            "Drive ID" : i.id,
            "Drive Conducted By" : company.company_name,
            "Job Role" : i.job_title,
            "Job Description" : i.job_description,
            "No.of Applied" : total_applied,
            "No.of Selected People" : total_selected
        })
    return make_response(jsonify(result),200)
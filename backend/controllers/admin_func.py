from flask import request,jsonify,make_response
from main import app
from controllers.user_datastore import user_datastore
from flask_security import utils , auth_required, roles_required
from model.models import *
from sqlalchemy import or_
from sqlalchemy import func
from datetime import datetime,date

@app.route('/api/registered_companies',methods=['GET'])
@auth_required('token')
@roles_required('admin')
def all_companies():
    companies = db.session.query(Company).filter(Company.approval_status=='pending').all()
    print(companies)
    result=[]
    for company in companies:
        result.append({
            "company_id" : company.id,
            "user_id" : company.user_id,
            "company_name" : company.company_name,
            "hr_contact" : company.hr_contact,
            "website" : company.website,
            "mediater" : company.user.name,
            "email" : company.user.email,
            "status" : company.approval_status
        })
    return make_response(jsonify(result),200)

@auth_required('token')
@roles_required('admin')
@app.route('/api/approve_company/<int:company_id>',methods=['PUT'])
def approve_company(company_id):
    company = db.session.query(Company).filter(Company.id==company_id).first()
    print(company)
    if(not company):
        result = {
            'message' :"Company with entered id not found !!!"
        }
        return make_response(jsonify(result),404)
    company.approval_status = "approved"
    db.session.commit()
    result = {
        "message":"Successfully changed the details of the company",
        "approval_status" : company.approval_status
    }
    return make_response(jsonify(result),200)


@app.route('/api/registered_students',methods=['GET'])
@auth_required('token')
@roles_required('admin')
def all_students():
    students = db.session.query(Student).filter(Student.status=='pending').all()
    result = []
    for i in students:
        result.append(
            {
                "id" : i.id,
                "name" : i.user.name,
                "email" : i.user.email,
                "roles" : [j.name for j in i.user.roles],
                "year" : i.year,
                "branch" : i.branch,
                "cgpa" : i.cgpa,
            }
        )
    return make_response(jsonify(result),200)


@app.route('/api/approve_student/<int:student_id>',methods=['PUT'])
@auth_required('token')
@roles_required('admin')
def approve_student(student_id):
    student = db.session.query(Student).filter(Student.id==student_id).first()
    if(not student):
        output = {
            "message" : "student with entered Id not found !!!"
        }
        return make_response(jsonify(output),404)

    student.status = 'approved'
    db.session.commit()
    return make_response(
        jsonify({
            "message" : "Successfully approved the student with ID " + str(student_id) + " !!!"
        }),200
    )


@app.route('/api/approved_companies',methods=['GET'])
@auth_required('token')
@roles_required('admin')
def approved_companies():
    approved_companies = db.session.query(Company).filter(Company.approval_status=='approved').all()
    result = []
    for i in approved_companies:
        result.append(
            {
                "company_id" : i.id,
                "company_name" : i.company_name,
                "hr_contact" : i.hr_contact,
                "website" : i.website,
                "mediater" : i.user.name,
                "email" : i.user.email,
                "status" : i.approval_status
            }
        )
    print(result)
    return make_response(jsonify(result),200)


@app.route('/api/change_to_blacklist/<int:company_id>',methods=['PUT'])
@auth_required('token')
@roles_required('admin')
def change_to_blacklist(company_id):
    company = db.session.query(Company).filter(Company.id==company_id).first()
    if(not company):
        result = {
            "message" : "company not found to edit !!!"
        }
        return make_response(jsonify(result),404)
    company.approval_status = "blacklist"
    db.session.commit()
    result = {
        "message" : "Successfully changes the status of the company with id " + str(company_id) + " to blacklist !!!"
    }
    return make_response(jsonify(result),200)


@app.route('/api/change_to_blacklist_student/<int:student_id>',methods=['PUT'])
@auth_required('token')
@roles_required('admin')
def change_to_blacklist_student(student_id):
    student = db.session.query(Student).filter(Student.id==student_id).first()
    print(student)
    if(not student):
        result = {
            "message" : "student not found to edit !!!"
        }
        return make_response(jsonify(result),404)
    student.status = "blacklist"
    db.session.commit()
    result = {
        "message" : "Successfully changes the status of the student with id " + str(student_id) + " to blacklist !!!"
    }
    return make_response(jsonify(result),200)


@app.route('/api/approved_students',methods=['GET'])
@auth_required('token')
@roles_required('admin')
def approved_students():
    approved_students = db.session.query(Student).filter(Student.status=='approved').all()
    result = []
    for i in approved_students:
        result.append(
            {
                "id" : i.id,
                "name" : i.user.name,
                "email" : i.user.email,
                "roles" : [j.name for j in i.user.roles],
                "year" : i.year,
                "branch" : i.branch,
                "cgpa" : i.cgpa,
                "status" : i.status
            }
        )
    return make_response(jsonify(result),200)


@app.route('/api/admin_search',methods=['GET'])
@auth_required('token')
@roles_required('admin')
def admin_search():
    searching_on = request.args.get('type')
    searching_value = request.args.get('query')
    if(not searching_on or not searching_value):
        return make_response(jsonify({
            "message" : "Required searching value and type to search !!!"
        }),400)
    if(searching_on == 'student'):
        students = db.session.query(Student).filter(Student.status != 'blacklist').all()
        result = []
        for i in students:
            if(searching_value.lower() in i.user.name.lower()):
                result.append(
                    {
                        "id" : i.id,
                        "name" : i.user.name,
                        "email" : i.user.email,
                        "roles" : [j.name for j in i.user.roles],
                        "year" : i.year,
                        "branch" : i.branch,
                        "cgpa" : i.cgpa,
                        "status" : i.status
                    }
                )
        print(result)
        return make_response(jsonify(result),200)
    
    if(searching_on=='company'):
        companies = db.session.query(Company).filter(Company.approval_status != 'blacklist').all()
        result = []
        for i in companies:
            if(searching_value.lower() in i.company_name.lower()):
                result.append(
                    {
                        "company_id" : i.id,
                        "company_name" : i.company_name,
                        "hr_contact" : i.hr_contact,
                        "website" : i.website,
                        "mediater" : i.user.name,
                        "email" : i.user.email,
                        "status" : i.approval_status
                    }
                )
        print(result)
        return make_response(jsonify(result),200)
    
@app.route('/api/get_drives_admin',methods=['GET'])
@auth_required('token')
@roles_required('admin')
def get_drives():
    today = date.today()
    ongoing_placements = db.session.query(PlacementDrive).filter(PlacementDrive.status=='approved',func.date(PlacementDrive.application_deadline)>=today).all()
    result = []
    for i in ongoing_placements :
        company_details = db.session.query(Company).filter(Company.id == i.company_id).first()
        print(i.job_title)
        result.append({
            "drive_id" : i.id,
            "company_name" : company_details.company_name,
            "Job_Role" : i.job_title,
            "Job_Description" : i.job_description
        })
    return make_response(jsonify(result),200)

@app.route('/api/update_drive',methods=['PUT'])
@auth_required('token')
@roles_required('admin')
def update_drive():
    data = request.get_json()
    if(not data):
        output = {
            "message" : "Data is required !!!"
        }
        return make_response(jsonify(output),400)
    drive_id = int(data.get('drive_id'))
    if(not drive_id):
        output = {
            "message" : "required drive_id !!!"
        }
        return make_response(jsonify(output),400)
    drive = db.session.query(PlacementDrive).filter(PlacementDrive.id == drive_id).first()
    if(not drive):
        output = {
            "message" : "drive is not available with drive_id !!!"
        }
        return make_response(jsonify(output),404)
    drive.status = 'closed'
    db.session.commit()
    output = {
        "message" : "Successfully closed the drive with id " + str(drive_id) + " !!!"
    }
    return make_response(jsonify(output),200)

@app.route('/api/get_all_applications',methods=['GET'])
@auth_required('token')
@roles_required('admin')
def get_all_applications():
    applications = db.session.query(Application).all()
    result = []
    for i in applications:
        company = db.session.query(Company).filter(Company.id==i.drive.company_id).first()
        result.append({
            "application_id" : i.id,
            "student_id" : i.student_id,
            "drive_id" : i.drive_id,
            "application_date" : i.application_date,
            "status" : i.status,
            "student_name" : i.student.user.name,
            "company_name" : company.company_name,
            "job_title" : i.drive.job_title,
            "cgpa" : i.student.cgpa,
            "branch" : i.student.branch,
            "year" : i.student.year
        })
    return make_response(jsonify(result),200)
# window.location.href = url 
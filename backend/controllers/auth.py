from flask import request,jsonify,make_response
from flask_security import utils
from flask_security.utils import verify_password,hash_password
from main import app 
from controllers.user_datastore import user_datastore
from controllers.database import db
from model.models import Student,Company

@app.route('/api/student_register',methods=['POST'])
def student_register():
    data = request.get_json()
    user_found = user_datastore.find_user(email=data['email'])
    if(user_found):
        data = {
            "message" : "User already Exists !!! Use Different Email To Register"
        }
        return make_response(jsonify(data),400)
    user_datastore.create_user(
        name = data['name'],
        email = data['email'],
        password = hash_password(data['password']),
        roles = ['student'],
    )
    db.session.commit()
    user_created = user_datastore.find_user(email=data['email'])
    new_student = Student(
        user_id = user_created.id,
        branch = data['branch'].lower(),
        cgpa = float(data['cgpa']),
        year = int(data['year']),
        status = 'pending'
    )
    db.session.add(new_student)
    db.session.commit()
    data = {
        "message":"Student Successfully Registered !!!",
        "user_name" : user_created.name,
        "email" : user_created.email,
        "branch" : user_created.student_profile.branch,
        "cgpa" : user_created.student_profile.cgpa,
        "year" : user_created.student_profile.year
    }
    return make_response(jsonify(data),200)


@app.route('/api/company_register',methods=['POST'])
def company_register():
    data = request.get_json()
    user_found = user_datastore.find_user(email=data['email'])
    if(user_found):
        data = {
            "message" : "User already Exists !!! Use Different Email To Register"
        }
        return make_response(jsonify(data),400)
    
    company_found = db.session.query(Company).filter(Company.company_name == data['company_name'].lower()).first()
    if(company_found):
        data = {
            "message" : "Company already Exists !!! Use Different Company Name To Register"
        }
        return make_response(jsonify(data),400)
    company_phone = db.session.query(Company).filter(Company.hr_contact == data['hr_contact']).first()
    if(company_phone):
        data = {
            "message" : "Phone Number already exists !!! Use Different phone number  To Register"
        }
        return make_response(jsonify(data),400)
    user_datastore.create_user(
        name = data['name'],
        email = data['email'],
        password = hash_password(data['password']),
        roles = ['company']
    )
    db.session.commit()
    user_created = user_datastore.find_user(email=data['email'])
    print(type(data['hr_contact']))
    if(len(str(data['hr_contact']))>10):
        data = {
            "message" : "please enter phone number length value lesser than 11 !!!"
        }
        return make_response(jsonify(data),400)
    
    new_company = Company(
        user_id = user_created.id,
        company_name = data['company_name'].lower(),
        hr_contact = int(data['hr_contact']),
        website = data['website'],
        approval_status = 'pending'
    )
    db.session.add(new_company)
    db.session.commit()
    data = {
        "message":"Company Successfully Registered !!!",
        "user_name" : user_created.name,
        "email" : user_created.email,
        "company_name" : user_created.company_profile.company_name,
        "hr_contact" : user_created.company_profile.hr_contact,
        "website" : user_created.company_profile.website,
        "approval_status" : user_created.company_profile.approval_status
    }
    return make_response(jsonify(data),200)


@app.route('/api/user_login',methods=['POST'])
def user_login():
    data = request.get_json()
    user_found = user_datastore.find_user(email=data['email'])
    if(user_found):
        if(not verify_password(data['password'],user_found.password)):
            output = {
                "message" : "Password incorrect !!!"
            }
            return make_response(jsonify(output),400)
        else:
            output=None
            utils.login_user(user_found)
            auth_token = user_found.get_auth_token()
            print(auth_token)
            if(user_found.roles[0]=='student'):
                output = {
                    "message" : "Successful login by Student !!!",
                    "name" : user_found.name,
                    "email" : user_found.email,
                    "roles" : [i.name for i in user_found.roles],
                    "branch" : user_found.student_profile.branch,
                    "cgpa" : user_found.student_profile.cgpa,
                    "year" : user_found.student_profile.year,
                    "auth_token" : auth_token,
                    "status" : user_found.student_profile.status
                }
            elif(user_found.roles[0]=='company'):
                output = {
                    "message" : "Successful login by Company !!!",
                    "name" : user_found.name,
                    "email" : user_found.email,
                    "roles" : [i.name for i in user_found.roles],
                    "company_name" : user_found.company_profile.company_name,
                    "hr_contact" : user_found.company_profile.hr_contact,
                    "website" : user_found.company_profile.website,
                    "auth_token" : auth_token,
                    "status" : user_found.company_profile.approval_status,
                    "company_id" : user_found.company_profile.id
                }
            elif(user_found.roles[0]=='admin'):
                output = {
                    "message" : "Successful login by Admin !!!",
                    "name" : user_found.name,
                    "email" : user_found.email,
                    "roles" : [i.name for i in user_found.roles],
                    "auth_token" : auth_token
                }

            return make_response(jsonify(output),200)
    return make_response(jsonify({
        "message" : "You have to register first !!!"
    }),404)
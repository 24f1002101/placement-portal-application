from flask_security import RoleMixin,UserMixin
from controllers.database import db

class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255),nullable=False)
    email  = db.Column(db.String(255),nullable=False,unique=True)
    password = db.Column(db.String(255),nullable=False)
    fs_uniquifier = db.Column(db.String(255),unique = True,nullable = False)
    fs_token_uniquifier = db.Column(db.String(255),unique=True)
    active = db.Column(db.Boolean(),default=True)
    roles = db.relationship('Role',secondary='user_role',backref="users")
    student_profile = db.relationship('Student',backref="user",uselist=False)
    company_profile = db.relationship('Company',backref='user',uselist=False)

class Role(db.Model,RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255),nullable=False)
    description = db.Column(db.String(255))

class User_role(db.Model):
    __tablename__ = 'user_role'
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    role_id = db.Column(db.Integer,db.ForeignKey("role.id"))

class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),unique=True)
    branch = db.Column(db.String(255),nullable=False)
    cgpa = db.Column(db.Float,nullable=False)
    year = db.Column(db.Integer,nullable=False)
    status = db.Column(db.String(255),nullable=False)
    
class Company(db.Model):
    __tablename__="company"
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),unique=True)
    company_name = db.Column(db.String(255),nullable=False)
    hr_contact = db.Column(db.String(255),nullable=False)
    website = db.Column(db.String(255))
    approval_status = db.Column(db.String(75),nullable=False)
    drives = db.relationship('PlacementDrive',backref="company")

class PlacementDrive(db.Model):
    __tablename__="placement_drive"
    id = db.Column(db.Integer,primary_key=True)
    company_id = db.Column(db.Integer,db.ForeignKey('company.id'))
    job_title = db.Column(db.String(255),nullable=False)
    job_description = db.Column(db.String(255),nullable=False)
    eligibility_branch = db.Column(db.String(200),nullable=False)
    eligibility_cgpa = db.Column(db.Float,nullable=False)
    eligibility_year = db.Column(db.Integer,nullable=False)
    application_deadline = db.Column(db.DateTime,nullable=False)
    status = db.Column(db.String(50), nullable=False)
    applications = db.relationship("Application",backref="drive")

class Application(db.Model):
    __tablename__ = "application"
    id = db.Column(db.Integer,primary_key=True)
    student_id = db.Column(db.Integer,db.ForeignKey('student.id'))
    drive_id = db.Column(db.Integer,db.ForeignKey('placement_drive.id'))
    application_date = db.Column(db.DateTime,nullable=False)
    status = db.Column(db.String(75),nullable=False)
    resume_path = db.Column(db.String(255), nullable=False)
    student = db.relationship("Student",backref="applications")
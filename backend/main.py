from flask import Flask
from controllers.config import Config
from controllers.database import db
from flask_migrate import Migrate
from flask_security import Security
from flask_restful import Api
from controllers.user_datastore import user_datastore
from flask_cors import CORS
from flask_security import hash_password
from datetime import datetime
from model.models import *
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
Migrate(app,db)
Security(app,user_datastore)
Api(app)
CORS(app)
with app.app_context():
        #db.create_all()
        admin_role = user_datastore.find_or_create_role(name='admin',description='Admin Role')
        company_role = user_datastore.find_or_create_role(name='company',description='Company Member')
        student_role = user_datastore.find_or_create_role(name='student',description='Student Role')
        admin = user_datastore.find_user(email='alambalaji1972@gmail.com')
        if(not admin):
            user_datastore.create_user(
                name='Alam Balaji',
                email="alambalaji1972@gmail.com",
                password=hash_password("AlamBalaji_1972"),
                roles = [admin_role]                     
            )
            db.session.commit()

from controllers.admin_func import *
from controllers.auth import *
from controllers.company_func import *
from controllers.student_func import *
if(__name__=="__main__"):
    app.run(debug=True)
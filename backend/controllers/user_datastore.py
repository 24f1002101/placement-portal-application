from flask_security import SQLAlchemyUserDatastore
from model.models import *
from controllers.database import db

user_datastore = SQLAlchemyUserDatastore(db,User,Role)
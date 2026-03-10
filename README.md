# placement-portal-application
Overview and Features:
  1. This Placement Portal consists of three roles(System Admin , Company , Student) .
  2. This Placement Portal allows Company and Student Roles to register and login but for the Admin Role only login is             allowed .
  3. This Placement Portal allows Admin to approve/blacklist companies,students , search companies and students , view             ongoing company drives , mark the ongoing drives as complete , view student applications and their resumes .
  4. This Placement Portal allows Company to create Drive , view ongoing drives and closed drives , mark the ongoing drives        as complete , view student applications for a particular drive , view resumes of them and select or reject them .
  5. This Placement Portal allows Student view ongoing drives , apply for the ongoing drives , upload resume , view                application history , edit profile .

Technologies Used
  1.Flask: Python web framework for backend logic by building REST API's.
  2.SQLAlchemy: ORM for managing database relationships and queries.
  3.Vue.js and Bootstrap : used for Frontend purpose.
  4.SQLite: Database for data persistence.
  5.Redis and Celery: Used for async Backend Jobs like generating CSV file , sending emails.

Installation
  1.Clone the repository:
      1. git clone https://github.com/24f1002101/placement-portal-application.git
      2. cd placement-portal-application
      3. creating virtual environement by the command python3 -m venv <venv_name>
      4. source <venv_name>/bin/activate
      5. pip install -r requirements.txt
  2. Running the Application:
      1. Running Backend : cd backend , and run python3 main.py
      2. Running Frontend : cd frontend , and run npm install and then npm install bootstrap , and then npm run dev
      3. Running redis server : run redis-server
      4. Running MailHog : MailHog
      5. Running celery worker tasks(CSV Generation) : cd backend,and then celery -A celery_app.celery worker --loglevel=info
      6. Running celery beat jobs(sending emails) : cd backend,and then celery -A celery_app.celery beat --loglevel=info
      7. the frontend port will be running at http://localhost:5173/ . Copy it and look the application on the supported               browser.
      

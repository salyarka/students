Description:
	This web app provides CRUD student and discipline management,
	uses builtin Flask server. The database schema is presented in
	schema.sql file.
Requirements:
	- Linux
	- Python 3
	- PostgreSQL 9.5.5
Before running the application, you need:
	- Install libraries ``pip install -r requirements.txt``
	- Export following variables to environment, which containes
	  credentials for database connection (DB_NAME, DB_USERNAME, DB_PASSWORD),
	  you can use shell script (credentials.sh) by replacing example credentials in it
	  with your credentials, and run script with command ``source ./credentials.sh``
	- Run simple test to check the connection to database ``python run.py test``
	- Create tables with command ``python run.py db init`` or ``python run.py db fill``
	  the difference between commands is that the first command creates blank tables and
	  second command creates tables with 1 million scores
	- Run app with command ``python run.py runserver``, by default app will be available
	  at adrress http://127.0.0.1:5000/
Usage:
	- At Discipline page you can manage disciplines
	- At Students page you can manage students (one the page there is pagination with
	  15 students per page, you can navigate with next or previous links if number of students
	  are higher than 15)
	- By clicking the student link you will be rederected to the student page, where you
	  can manage each student and his scores
	- At Search students page you can search students by name (pagination like Students page)


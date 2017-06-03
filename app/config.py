import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    dbname = os.environ.get('DB_NAME')
    user = os.environ.get('DB_USERNAME')
    password = os.environ.get('DB_PASSWORD')
    DATABASE = {'dbname': dbname, 'user': user, 'password': password}

class Test(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False

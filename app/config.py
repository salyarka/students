import os


class Config:
    dbname = os.environ.get('DB_NAME')
    user = os.environ.get('DB_USERNAME')
    password = os.environ.get('DB_PASSWORD')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE = {'dbname': dbname, 'user': user, 'password': password}


class Develop(Config):
    DEBUG = True


class Test(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False


config = {
    'standard': Config,
    'develop': Develop,
    'testing': Test
}
import os


class DefaultConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')

class TestingConfig(DefaultConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    
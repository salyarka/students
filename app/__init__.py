import os
from flask import Flask
from flask_script import Manager
from app.db import DB
from .config import config
from flask_modus import Modus


app = Flask(__name__)
app.config.from_object(config[os.getenv('FLASK_CONFIG') or 'develop'])
modus = Modus(app)
db = DB(app)

from app import views

import os
from flask import Flask
from flask_script import Manager
from flask_modus import Modus
from .config import config
from app.db import DB


app = Flask(__name__)
app.config.from_object(config[os.getenv('FLASK_CONFIG') or 'standard'])
modus = Modus(app)
db = DB(app)

from app import views

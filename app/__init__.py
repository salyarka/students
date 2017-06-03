from flask import Flask
from flask_script import Manager
from app.db import DB
# from flask_modus import Modus


app = Flask(__name__)
# modus = Modus(app)
manager = Manager(app)
app.config.from_object('app.config.Config')
db = DB(app)


from app import views
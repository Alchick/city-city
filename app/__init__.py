from flask import Flask
#from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from flask.ext.compress import Compress
from flask.ext.cache import Cache
import sys
import logging, logging.config
logging.config.fileConfig('logging.conf')

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.config.from_object('config')
Compress(app)

mail = Mail(app)
db = SQLAlchemy(app)
from app import views, models

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(models.culture_admins).filter(models.culture_admins.id == user_id).first()


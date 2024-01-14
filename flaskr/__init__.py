from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from flaskr.config import Config


app = Flask(__name__, static_folder='static')
app.config.from_object(Config)

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'access_bp.login'
# default login_manager.login_message = ''
login_manager.login_message_category = 'warning'


# Importa le funzioni di vista per registrare le rotte
from flaskr import views

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from const import CSV_DIR
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__, static_folder='static')
app.config['UPLOAD_DIRECTORY'] = CSV_DIR
app.config['ALLOWED_EXTENSIONS'] = ['.csv']
app.config['SECRET_KEY'] = '7b8245da186ff6cf3d8321ce21119683'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Importa le funzioni di vista per registrare le rotte
from flaskr import views

from flask import Flask
from utils import *

app = Flask(__name__, static_folder='static')
app.config['UPLOAD_DIRECTORY'] = CSV_DIR
app.config['ALLOWED_EXTENSIONS'] = ['.csv']


# Importa le funzioni di vista per registrare le rotte
from .views import *

# Questo import è necessario per evitare circolarità nelle dipendenze
from . import views

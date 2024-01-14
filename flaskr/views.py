from flaskr import app

from flaskr.routes.root_errors.routes import root_errors_bp
from flaskr.routes.access.routes import access_bp
from flaskr.routes.interface.routes import interface_bp
from flaskr.routes.api.routes import api_bp
from flaskr.utility.file_system import FileSystem


"""
fonti per capire blueprint
https://realpython.com/flask-blueprint/
https://www.freecodecamp.org/news/how-to-use-blueprints-to-organize-flask-apps/

per differenziare dalla cartella static principale
https://stackoverflow.com/questions/41853436/flask-raises-404-for-blueprint-static-files-when-using-blueprint-static-route

in generale per dividere il codice (blueprint, ereditare html, db)
https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy
"""

# DO NOT REMOVE
# FILE SYSTEM MODULE FOR DATA
# first occurence of this module singleton
# it checks that directories for data exists
file_system = FileSystem()

"""
blueprint name: root_errors_bp
for routes:
/
404 (all app)
"""
app.register_blueprint(root_errors_bp)


"""
blueprint name: access_bp
for routes:
/login
/register
"""
app.register_blueprint(access_bp)


"""
blueprint name: interface_bp
for routes:
/logout
/models_creator
"""
app.register_blueprint(interface_bp)


"""
blueprint name: api_bp
for routes with /api:
/delete
/saving
"""
app.register_blueprint(api_bp, url_prefix='/api')


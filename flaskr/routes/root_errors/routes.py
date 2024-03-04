from flask import Blueprint
from flask import render_template, redirect, url_for, request, jsonify

# Defining a blueprint
root_errors_bp = Blueprint(
    'root_errors_bp',
    __name__,
    template_folder='templates',
    static_folder='static',
    #static_url_path='/errors'
)

"""
per gestire gli errori della applicazione in generale e non solo di un blueprint
si usa .app_errorhandler e non errorhandler
il secondo si riferisce all'interno del blueprint
se invece è fatto con @app.errorhandler si riferisce a tutta l'app
https://stackoverflow.com/questions/58728366/python-flask-error-handling-with-blueprints
"""


@root_errors_bp.route('/')
def index():
    return redirect(url_for('access_bp.login'))


@root_errors_bp.route('/favicon.ico')
def favicon():
    return redirect('/static/favicon.ico')


@root_errors_bp.app_errorhandler(404)
def not_found(e):
  if request.path.startswith('/api'):
     return jsonify({'error': 404})
  return render_template('pages/general.html', e=e), 404

@root_errors_bp.app_errorhandler(403)
def not_found(e):
  if request.path.startswith('/api'):
     return jsonify({'error': 403})
  return render_template('pages/general.html', e=e), 403

@root_errors_bp.app_errorhandler(500)
def not_found(e):
  if request.path.startswith('/api'):
     return jsonify({'error': 500})
  return render_template('pages/general.html', e=e), 500

"""
@root_errors_bp.app_errorhandler(Exception)
def general_error(e):  
  # e.code = 404
  # e.description = 'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.'
  # e.name = 'Not Found'
  
  #print(e)
  return render_template('pages/general.html', e=e)
"""
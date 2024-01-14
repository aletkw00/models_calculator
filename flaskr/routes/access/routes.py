from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user

from flaskr.models import User
from flaskr.routes.access.forms import LoginForm, RegistrationForm
from flaskr import db, bcrypt

from flaskr.utility.file_system import FileSystem

# Defining a blueprint
access_bp = Blueprint(
    'access_bp',
    __name__,
    template_folder='templates',
    static_folder='static',
    #static_url_path='/access'
)


# FILE SYSTEM MODULE FOR DATA
file_system = FileSystem()


@access_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('access_bp.login'))


@access_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('interface_bp.dashboard'))
    """ Check the if user exist and then redirect them to the application page 
    """
    form = LoginForm()
    if form.validate_on_submit():
        user: User = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page == None:
                return redirect(url_for('interface_bp.dashboard'))
            else:
                return redirect(next_page)
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            return redirect(url_for('access_bp.login'))
    return render_template('pages/login.html', title='Login', form=form)


@access_bp.route('/register', methods=['GET', 'POST'])
def register():    
    if current_user.is_authenticated:
        return redirect(url_for('interface_bp.dashboard'))
    """ Create a user account and then create his folder in 'dir_of_models'
    """
    form = RegistrationForm()
    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        file_system.create_path_user(user.id)

        flash(f'Account created! Now you are able to log in', 'success')
        return redirect(url_for('access_bp.login'))
    return render_template('pages/register.html', title='Registrazione', form=form)

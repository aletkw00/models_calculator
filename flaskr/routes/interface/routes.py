from flask import Blueprint
from flask import render_template, flash, redirect, url_for, session, request
from flask_login import login_required, current_user

from flaskr.routes.interface.forms import AccountForm, ModelForm
from flaskr.utility.file_system import FileSystem
#from flaskr.utility.run_scripts import GenerateRegressionModel
from flaskr.models import User
from flaskr import db, bcrypt

# Defining a blueprint
interface_bp = Blueprint(
    'interface_bp',
    __name__,
    template_folder='templates',
    static_folder='static',
    #static_url_path='/interface'
)

# FILE SYSTEM MODULE FOR DATA
filesystem = FileSystem()


@interface_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('pages/dashboard.html')


@interface_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = AccountForm()
    if request.method == 'GET':
        form.email.data = current_user.email
        #form.password.data = current_user.password
    elif request.method == 'POST':
        if form.validate_on_submit():
            current_user.email = form.email.data
            if form.password.data != "":
                current_user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            db.session.commit()
            flash('Data updated', category='success')
            return redirect(url_for('interface_bp.account'))

    return render_template('pages/account.html', form=form)


@interface_bp.route('/file_manager')
@login_required
def file_manager():
    return render_template('pages/file_manager.html')


@interface_bp.route('/regression_calculator', methods=['GET', 'POST'])
@login_required
def regression_calculator():
    form = ModelForm()
    vis_dir = filesystem.get_visible_directory(current_user.id)
    phase = 0
    window = ''
    test = False
    session['runned'] = False
    if request.method == 'POST':
        if form.validate_on_submit():
            # Get the name of the directory of the model
            session['model_dir'] = filesystem.get_secure_filename(request.form.get('model_dir'))            

            # Get the files
            file1 = request.files['file_input']
            files = request.files.getlist("files_output")

            # Checking extensions of files
            check_result = filesystem.check_files_extension(file1, files)
            if check_result != None:
                flash(check_result, 'danger')
                phase = 1 # show error on phase 1, do not start running
                return render_template('pages/regressionCalculator.html', model_dirs=vis_dir, form=form, phase=phase)

            # Iterate for each file in the files List, and Save them
            filesystem.save_a_uploaded_input(file1,current_user.id)

            filesystem.save_all_uploaded_output(files,current_user.id)

            session['filename'] = filesystem.get_time_secure_filename(request.form.get('modelname')) # type: ignore
            window = str(request.form.get('window'))
            test = bool(request.form.get('test'))
            phase = 2 # start running

            #return redirect(url_for('interface_bp.regression_calculator'))
        else:
            phase = 1 # show error on phase 1, do not start running
            return render_template('pages/regressionCalculator.html', model_dirs=vis_dir, form=form, phase=phase)

    return render_template('pages/regressionCalculator.html', model_dirs=vis_dir, form=form, phase=phase, data_window=window, data_test=test)


@interface_bp.route('/about')
@login_required
def about():
    return render_template('pages/about.html')
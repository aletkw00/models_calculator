import ipaddress
import shutil
import json
from flask import jsonify, request, render_template, flash, redirect, url_for, session
from werkzeug.utils import secure_filename
from flaskr import app, db, bcrypt
from flask_login import login_user, logout_user, login_required
import os
import subprocess
from const import *
from flaskr.models import User
from flaskr.login import RegistrationForm, LoginForm, ModelForm


def move_file(source_path, destination_path):
    shutil.move(source_path, destination_path)

def get_visible_directory(path):
    directory = [folder for folder in os.listdir(path) 
               if os.path.isdir(os.path.join(path, folder)) 
               and not folder.startswith('.')]
    return directory

def json_response(status, message):
    response_data = {
        'status': status,
        'message': message
    }
    return jsonify(response_data)

def modal(host_name, password, Ip, topic, path):
    """Creates the configuration file for the broker if the input values are valid.    
    """
    try:
        Ip = str(ipaddress.ip_address(Ip))
    except ValueError:
        error_message = 'Invalid Ip Address'
        return json_response('failure', error_message)
    
    if not os.path.exists(path):
        error_message = 'Model directory not exist, Please select an existing one'
        return json_response('failure', error_message)
    
    # Create a dictionary with the data
    data = {
        'username': host_name,
        'password': password,
        'host': Ip,
        'topic-ricezione': topic
    }

    # Save the data to a new JSON file
    with open(os.path.join(path, 'config.json'), 'w') as file:
        json.dump(data, file)

    return json_response('success', 'Data saved successfully.')

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/models_creator', methods=['GET','POST'])
@login_required
def models_creator():
    
    form = ModelForm()
    vis_dir = get_visible_directory(session['user_path'])
    if request.method == 'POST':
        if form.validate_on_submit():
            # Get the name of the directory of the model
            session['model_dir'] = secure_filename(request.form.get('model_dir'))
            model_dir = os.path.join(session['user_path'], session['model_dir'])
            

            # Get the files
            file1 = request.files['file1']
            files = request.files.getlist("file2")


            # Checking extensions of files
            extension1 = os.path.splitext(file1.filename)[1]
            if extension1 not in app.config['ALLOWED_EXTENSIONS']:
                flash('Input file not CSV file', 'danger')
                return render_template('index.html', model_dirs=vis_dir, form=form)
            
            for file2 in files:
                extension2 = os.path.splitext(file2.filename)[1]
                if extension2 not in app.config['ALLOWED_EXTENSIONS']:
                    flash('Output file(s) not CSV file', 'danger')
                    return render_template('index.html', model_dirs=vis_dir, form=form)
                    
                
            # Iterate for each file in the files List, and Save them
            i=1
            for file2 in files:
                file2.save(os.path.join(
                    app.config['UPLOAD_DIRECTORY'],
                    'st' + str(i) + '_' + OUTPUT_FILE))
                i+=1

            file1.save(os.path.join(
                app.config['UPLOAD_DIRECTORY'],
                INPUT_FILE))

            window = str(request.form.get('window'))
            
            session['filename'] = secure_filename(request.form.get('modelname'))
            test = '-test' if request.form.get('test') else ''

            path_tmp_models_dir = os.path.join(session['user_path'], TMP_MODELS_DIRECTORY)

            # Command to execute as command line
            command = [
                'python3', 
                'models_creator.py', 
                app.config['UPLOAD_DIRECTORY'], 
                path_tmp_models_dir
            ]

            # Adding flags to the command
            if window != '':
                window = '-i' + window
                command.append(window)
            if session['filename'] !='':
                filename = '-o' + session['filename']
                command.append(filename)
            if test != '':
                command.append(test)
            # Run the script
            try:
                result = subprocess.run(command, capture_output=True, text=True)

                if result.returncode == 0:
                    generated_string = result.stdout.strip()
                else:
                    generated_string = f"Error: {result.stderr.strip()}"

            except subprocess.CalledProcessError:
                generated_string = 'Something went wrong with the script'
            finally:
                for filename in os.listdir(app.config['UPLOAD_DIRECTORY']):
                    file_path = os.path.join(app.config['UPLOAD_DIRECTORY'], filename)
                    if os.path.isfile(file_path) and filename != '.gitkeep':
                        os.remove(file_path)
                session['runned'] = True
                # Check if directory alredady exists, if not create
                if not os.path.exists(model_dir):
                    os.makedirs(model_dir)
                session['generated_string'] = generated_string.strip()

            return redirect(url_for('models_creator'))
        
    generated_string = session.get('generated_string', '')

    return render_template('index.html', model_dirs=vis_dir, form=form, string=generated_string)



@app.route('/delete', methods=['POST'])
def delete_function():
    data = request.get_json()
    if data.get('output_content') == 'Processing...' or data.get('output_content') == '':
        error_message = 'Models not calculated yet'
        return json_response('failure', error_message)

    if session['runned'] == True:  
        if session['filename'] == '':
            filename = DEFAULT_MODEL_NAME
        else:
            filename = session['filename']
            
        model_dir = os.path.join(session['user_path'], session['model_dir'])
        tmp_model_dir_path = os.path.join(session['user_path'], TMP_MODELS_DIRECTORY)

        # Remove models from tmp user directory
        for file in os.listdir(tmp_model_dir_path):
            if file.startswith(filename):
                os.remove(os.path.join(tmp_model_dir_path, file))

        # Check if the directory previously created is empty. Eventually delete it
        if os.path.exists(model_dir) and os.path.isdir(model_dir):
            if not os.listdir(model_dir):
                os.rmdir(model_dir)
        session['runned'] = False
        session['generated_string'] = ''
        return json_response('success', 'All correct')
    else:
        error_message = 'Models not calculated yet'
        return json_response('failure', error_message)

@app.route('/saving', methods=['POST'])
def saving_function():
    data = request.get_json()
    if data.get('output_content') == 'Processing...':
        error_message = 'Models not calculated yet'
        return json_response('failure', error_message)
    
    

    if session['runned'] == False:
        
        session['model_dir'] = secure_filename(data.get('model_dir'))
        if session['model_dir'] == '':
            error_message = 'Select a model direcotry'
            return json_response('failure', error_message)
        else:
            session['filename'] == ''
    else:
        if session['filename'] == '':
            filename = DEFAULT_MODEL_NAME
        else:
            filename = session['filename']

    host_name = data.get('hostname')
    password = data.get('password')
    Ip = data.get('IP')
    topic = data.get('topic')

    model_dir = os.path.join(session['user_path'], session['model_dir'])

    # Create if possible the broker config file
    if all([host_name, password, Ip, topic]):
        response = modal(host_name, password, Ip, topic, model_dir)
        if response.json['status'] == 'failure':
            return response
    
    if session['runned'] == True:
    # Move models from tmp directory to the choosen one
        tmp_model_dir_path = os.path.join(session['user_path'], TMP_MODELS_DIRECTORY)
        for file in os.listdir(tmp_model_dir_path):
            if file.startswith(filename):
                move_file(os.path.join(tmp_model_dir_path, file),
                        os.path.join(model_dir, file))
    session['runned'] = False
    session['generated_string'] = ''
    return json_response('success', 'All correct')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """ Create an user account and then create his folder in 'dir_of_models'
    """
    form = RegistrationForm()
    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        create_path_user = os.path.join(MODEL_DIR, form.username.data)
        os.makedirs(create_path_user)
        create_tmp_path = os.path.join(create_path_user, TMP_MODELS_DIRECTORY)
        os.makedirs(create_tmp_path)
        with open(os.path.join(create_tmp_path, '.gitkeep'), 'w') as file:
            pass
        flash(f'Account created! Now you are able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form = form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Check the if user exist and then redirect them to the application page 
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            session['user_path'] = os.path.join(MODEL_DIR, form.username.data)
            session['runned'] = False
            session['generated_string'] = ''
            return redirect(url_for('models_creator'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
import ipaddress
import shutil
import json
from flask import jsonify, request, render_template
from werkzeug.utils import secure_filename
from . import app
import os
import subprocess
from const import *

user_path = os.path.join(MODEL_DIR, 'Padova')

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
    try:
        Ip = str(ipaddress.ip_address(Ip))
    except ValueError:
        error_message = 'Invalid Ip Address'
        return json_response('failure', error_message)
    
    # Create a dictionary with the data
    data = {
        'username': host_name,
        'password': password,
        'host': Ip,
        'topic-ricevi': topic
    }

    # Save the data to a new JSON file
    with open(os.path.join(path, 'nome_da_cambiare.json'), 'w') as file:
        json.dump(data, file)

    return json_response('success', 'Data saved successfully.')

@app.route('/')
def index():
    visible_directory = get_visible_directory(user_path)
    return render_template('index.html', model_dirs=visible_directory)


@app.route('/models_creator', methods=['GET','POST'])
def run_models_creation():
    #get the name of the directory of the model
    model_dir = secure_filename(request.form.get('model_dir'))
    model_dir = os.path.join(user_path, model_dir)

    #check if directory alredady exists, if not create
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    #get the 2 file
    file1 = request.files['file1']
    files = request.files.getlist("file2")


    #checking extensions of files
    extension1 = os.path.splitext(file1.filename)[1]
    if extension1 not in app.config['ALLOWED_EXTENSIONS']:
        return jsonify({'message': 'Input non è un file .csv'})
    
    for file2 in files:
        extension2 = os.path.splitext(file2.filename)[1]
        if extension2 not in app.config['ALLOWED_EXTENSIONS']:
            return jsonify({'message': 'Inserisci file .csv'})
        
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

    window = request.form.get('window')
    filename = secure_filename(request.form.get('filename'))
    test = '-test' if request.form.get('test') else ''

    path_tmp_models_dir = os.path.join(user_path, TMP_MODELS_DIRECTORY)

    command = [
        'python3', 
        'models_creator.py', 
        app.config['UPLOAD_DIRECTORY'], 
        path_tmp_models_dir
    ]

    if window != '':
        window = '-i' + window
        command.append(window)
    if filename !='':
        filename = '-o' + filename
        command.append(filename)
    if test != '':
        command.append(test)
    #run the script
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
            if os.path.isfile(file_path):
                os.remove(file_path)

    return jsonify({'message': generated_string})


@app.route('/delete', methods=['POST'])
def delete_function():

    data = request.get_json()
    model_dir = secure_filename(data.get('model_dir'))
    filename = secure_filename(data.get('filename'))
    if filename == '':
        filename = DEFAULT_MODEL_NAME
        
    model_dir = os.path.join(user_path, model_dir)
    tmp_model_dir_path = os.path.join(user_path, TMP_MODELS_DIRECTORY)
    for file in os.listdir(tmp_model_dir_path):
        if file.startswith(filename):
            os.remove(os.path.join(tmp_model_dir_path, file))

    # Se la cartella dove l'utente voleva salvare i modelli è vuota eliminala
    if os.path.exists(model_dir) and os.path.isdir(model_dir):
        if not os.listdir(model_dir):
            os.rmdir(model_dir)
    
    return json_response('success', 'All correct')

@app.route('/saving', methods=['POST'])
def saving_function():
    data = request.get_json()
    model_dir = secure_filename(data.get('model_dir'))
    filename = secure_filename(data.get('filename'))
    if filename == '':
        filename = DEFAULT_MODEL_NAME

    host_name = data.get('hostname')
    password = data.get('password')
    Ip = data.get('IP')
    topic = data.get('topic')

    model_dir = os.path.join(user_path, model_dir)

    if all([host_name, password, Ip, topic]):
        response = modal(host_name, password, Ip, topic, model_dir)
        if response.json['status'] == 'failure':
            return response
    
    tmp_model_dir_path = os.path.join(user_path, TMP_MODELS_DIRECTORY)
    for file in os.listdir(tmp_model_dir_path):
        if file.startswith(filename):
            move_file(os.path.join(tmp_model_dir_path, file),
                      os.path.join(model_dir, file))
    
    return json_response('success', 'All correct')

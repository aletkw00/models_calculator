from flask import Blueprint
from flask import jsonify, request, session, send_file, flash
from flask_login import current_user

from flaskr.utility.file_system import FileSystem
from flaskr.utility.run_scripts import DeleteFileTimer, GenerateRegressionModel


# Defining a blueprint
api_bp = Blueprint(
    'api_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)

"""
fonti
https://stackoverflow.com/questions/56546795/how-to-receive-files-in-javascript-sent-from-flask-using-send-file
https://stackoverflow.com/questions/53747258/flask-send-file-not-sending-file
https://stackoverflow.com/questions/59162890/javascript-button-to-download-zipfile-generated-by-python3-flask
https://www.tutorialspoint.com/How-to-create-a-zip-file-using-Python
https://stackoverflow.com/questions/58955341/create-zip-from-directory-using-python
"""

# FILE SYSTEM MODULE FOR DATA
filesystem = FileSystem()

@api_bp.route('/file_manager/getlist', methods=['POST'])
def getlist_function():
    idUser = current_user.id
    data = request.get_json()
    dict_dir = filesystem.get_directory_content(idUser, data.get('insideDir'))
    return jsonify(dict_dir)


@api_bp.route('/file_manager/get', methods=['POST'])
def get_download():    
    idUser = current_user.id
    data = request.get_json()
    path = data.get('path')
    isDir = data.get('isDir')
    if (isDir):
        #is a directory
        path, file_name = filesystem.download_a_dir(idUser, path)
        # PROCESS ASYNC TO DELETE THE ZIP CREATED
        # TO CHANGE THE TIME BEFORE DELETE GO TO THE CLASS
        DeleteFileTimer(path)
        return send_file(path_or_file=path, mimetype='application/octet-stream', as_attachment=True, download_name=file_name)
    else:
        #is a file
        path, file_name = filesystem.download_a_file(idUser, path)
        return send_file(path_or_file=path, mimetype='application/octet-stream', as_attachment=True, download_name=file_name)

@api_bp.route('/file_manager/delete', methods=['POST'])
def file_delete_function():
    idUser = current_user.id
    data = request.get_json()
    path = data.get('path')
    isDir = data.get('isDir')
    if (isDir):
        #is a directory
        name, result = filesystem.delete_tree_dir(idUser, path)
        return jsonify({name: result})
    else:
        #is a file
        name, result = filesystem.delete_a_file(idUser, path)
        return jsonify({name: result})

@api_bp.route('/file_manager/rename', methods=['POST'])
def files_rename_function():
    idUser = current_user.id
    data = request.get_json()
    oldpath = data.get('oldpath')
    newname = data.get('newname')
    isDir = data.get('isDir')
    if (isDir):
        #is a directory
        result = filesystem.rename_a_dir(idUser, oldpath, newname)
        #flash('Rinominato con ' + result, 'success')
        return jsonify({'name': result})
    else:
        #is a file
        result = filesystem.rename_a_file(idUser, oldpath, newname)
        #flash('Rinominato con ' + result, 'success')
        return jsonify({'name': result})


@api_bp.route('/regression_calculator/run', methods=['POST'])
def running_function():
    data = request.get_json()
    window = str(data.get('window'))
    test = data.get('test')

    path_tmp_models_dir = filesystem.get_path_tmp_models(current_user.id)

    # Command to execute as command line
    command_run_regression = GenerateRegressionModel(filesystem.get_path_upload(current_user.id),
                path_tmp_models_dir)

    # Adding flags to the command
    if window != '':
        command_run_regression.flag_window(window=window)
    if session['filename'] != '':
        command_run_regression.flag_filename(session['filename'])
    if test == True:
        command_run_regression.flag_test()

    # Run the script
    try:
        generated_string = command_run_regression.run_script()
        
    finally:
        filesystem.delete_all_uploaded_files(current_user.id)
        session['runned'] = True
        # File will be saved or deleted with an action button
        generated_string = generated_string.strip()

    # Save file to main dir
    if session['runned'] == True:
        # Check if model directory already exists, if not create
        path_model = filesystem.make_new_sub_dir(filesystem.get_path_user(current_user.id), session['model_dir'])
        path_tmp = filesystem.get_path_tmp_models(current_user.id)
        filesystem.move_result_tmp_to_model( path_model, path_tmp, session['filename'])
        session['runned'] = False
        result = {'saved': True, 'output': generated_string, 'directory': session['model_dir'], 'filename': session['filename']}
        return jsonify(result)
    else:
        return jsonify({'runned': False, 'output': generated_string})

    


from flask import Blueprint
from flask import jsonify, request, session, send_file
from flask_login import current_user

from flaskr.utility.file_system import FileSystem
from flaskr.utility.run_scripts import DeleteFileTimer


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
    if (data.get('isDir')):
        #is a directory
        path, file_name = filesystem.download_a_dir(idUser, data.get('path'))
        # PROCESS ASYNC TO DELETE THE ZIP CREATED
        # TO CHANGE THE TIME BEFORE DELETE GO TO THE CLASS
        DeleteFileTimer(path)
        return send_file(path_or_file=path, mimetype='application/octet-stream', as_attachment=True, download_name=file_name)
    else:
        #is a file
        path, file_name = filesystem.download_a_file(idUser, data.get('path'))
        return send_file(path_or_file=path, mimetype='application/octet-stream', as_attachment=True, download_name=file_name)

@api_bp.route('/file_manager/delete', methods=['POST'])
def file_delete_function():
    idUser = current_user.id
    data = request.get_json()
    if (data.get('isDir')):
        #is a directory
        name, result = filesystem.delete_tree_dir(idUser, data.get('path'))
        return jsonify({name: result})
    else:
        #is a file
        name, result = filesystem.delete_a_file(idUser, data.get('path'))
        return jsonify({name: result})

@api_bp.route('/file_manager/rename', methods=['POST'])


@api_bp.route('/regression_calculator/save', methods=['POST'])
def saving_function():
    data = request.get_json()

    if session['runned'] == True:
        # Check if model directory already exists, if not create
        path_model = filesystem.make_new_sub_dir(filesystem.get_path_user(current_user.id), session['model_dir'])
        path_tmp = filesystem.get_path_tmp_models(current_user.id)
        filesystem.move_result_tmp_to_model( path_model, path_tmp, session['filename'])
    else:
        return jsonify({'runned': 'false'})

    session['runned'] = False
    result = {'saved': True, 'directory': session['model_dir'], 'filename': session['filename']}
    return jsonify(result)



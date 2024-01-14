import os
import shutil
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from zipfile import ZipFile
from datetime import datetime
import pytz


from flaskr import app


def read_a_file_byte(path, name_file) -> bytes:
    with open(file=os.path.join(path, name_file), mode='rb',) as f:
        data = f.read()        
        return data


class FileSystem:
    # I WANT A SINGLETON OF THIS CLASS ON ENTIRE APP
    # https://stackoverflow.com/questions/12305142/issue-with-singleton-python-call-two-times-init
    # https://stackoverflow.com/questions/31269974/why-singleton-in-python-calls-init-multiple-times-and-how-to-avoid-it
    # https://www.geeksforgeeks.org/singleton-pattern-in-python-a-complete-guide/
    # 
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(FileSystem, cls).__new__(cls)
            cls.run_init = True
        return cls.instance
    
    # RUN ONLY ON FIRST ISTANCE
    def __init__(self) -> None:
        if (self.run_init):
            self.run_init=False
            # Directory
            # 
            self.root_run_dir = os.getcwd()
            self.root_data_dir_name = app.config['ROOT_DATA_DIR_NAME']
            self.allowed_extensions = app.config['ALLOWED_EXTENSIONS']
            self.dir_name_upload = '.uploads'
            self.dir_name_tmp_model = '.tmp_models_dir'
            self.file_name_for_integrity = '.keep'
            #self.path_upload = os.path.join(self.root_data_dir_name, self.dir_name_upload)
            # check if folder structure exists
            if not os.path.exists(self.root_data_dir_name):
                os.mkdir(self.root_data_dir_name)
            #if not os.path.exists(self.path_upload):
            #    os.mkdir(self.path_upload)
            # File
            #
            self.input_file = 'input.csv'
            self.output_file = 'output.csv'

    # IMPORTANT NOTES
    # On init is saved the current working dir.
    # When use os. with some functions such as mkdir or path.join
    # is not essential to use the working dir, because it is imped.
    # So is the same
    # os.mkdir(os.path.join(self.root_run_dir, sself.root_data_dir_name)
    # os.mkdir(self.root_data_dir_name)
    # to create the folder root_data_dir_name in the current working dir


    def create_path_user(self, id: int) -> None:
        # dir_of_models/(number)
        create_path_user = os.path.join(self.root_data_dir_name, str(id))
        os.mkdir(create_path_user)
        # dir_of_models/(number)/.tmp_models_dir
        create_tmp_path = os.path.join(create_path_user, self.dir_name_tmp_model)
        os.makedirs(create_tmp_path)
        with open(os.path.join(create_tmp_path, self.file_name_for_integrity), 'w') as file:
            pass
        # dir_of_models/(number)/.uploads
        create_upload_path = os.path.join(create_path_user, self.dir_name_upload)
        os.makedirs(create_upload_path)
        with open(os.path.join(create_upload_path, self.file_name_for_integrity), 'w') as file:
            pass


    def get_path_user(self, id: int) -> str:
        # dir_of_models/(number)
        return os.path.join(self.root_data_dir_name, str(id))


    def get_path_upload(self, id: int) -> str:        
        # dir_of_models/(number)/.uploads
        return os.path.join(self.get_path_user(id), self.dir_name_upload)
    

    def get_path_tmp_models(self, id: int) -> str:
        return os.path.join(self.get_path_user(id), self.dir_name_tmp_model)


    def get_visible_directory(self, id: int) -> list[str]:
        path = self.get_path_user(id)
        directory = [folder for folder in os.listdir(path)
                    if os.path.isdir(os.path.join(path, folder))
                    and not folder.startswith('.')]
        return directory
    

    def get_directory_content(self, id: int, dir: str) -> dict:
        path = self.get_path_user(id)
        if dir != '':
            path = os.path.join(path, dir)
        content_list = {}
        try:
            for content in os.listdir(path):
                if os.path.isdir(os.path.join(path, content)) and not content.startswith('.'):
                    content_list.update({content: True})
                elif not content.startswith('.'):
                    content_list.update({content: False})
        except FileNotFoundError:
            return {'No file':False}
        return content_list
    
    def get_secure_filename(self, dir: str) -> str:
        return secure_filename(dir)

    def get_time_secure_filename(self, dir: str) -> str:
        initial_filename = datetime.now(pytz.timezone('Europe/Rome')).strftime('%Y_%m_%d_%H_%M_%S')
        if dir == "":
            return initial_filename
        return initial_filename + "-" + secure_filename(dir)


    def check_files_extension(self, file1, files) -> str|None :
        extension1 = os.path.splitext(file1.filename)[1]
        if extension1 not in self.allowed_extensions:
            return 'Input file not CSV file'

        for file2 in files:
            extension2 = os.path.splitext(file2.filename)[1]
            if extension2 not in self.allowed_extensions:
                return 'Output file(s) not CSV file'
        return None


    def _save_a_file(self, file: FileStorage, path: str, name_file: str) -> None:
        file.save(os.path.join(path, name_file))



    def save_a_uploaded_input(self, file: FileStorage, id: int) -> None:
        self._save_a_file(file, self.get_path_upload(id), self.input_file)


    def save_all_uploaded_output(self, files: list[FileStorage], id: int) -> None:
        i = 1
        for file2 in files:
            self._save_a_file(file2,
                self.get_path_upload(id),
                'st' + str(i) + '_' + self.output_file)
            i += 1        


    def make_new_sub_dir(self, parent_exist: str, new_dir: str) -> str:
        new_path = os.path.join(parent_exist, new_dir)
        if not os.path.exists(new_path):
            os.mkdir(new_path)
            with open(os.path.join(new_path, self.file_name_for_integrity), 'w') as file:
                pass
        return new_path
    

    def delete_all_uploaded_files(self, id: int) -> None:
        for filename in os.listdir(self.get_path_upload(id)):
            file_path = os.path.join(self.get_path_upload(id), filename)
            if os.path.isfile(file_path) and filename != self.file_name_for_integrity:
                os.remove(file_path)


    def delete_a_file(self, id: int, dir: str) -> (str, str):        
        path = self.get_path_user(id)
        path = os.path.join(path, dir)
        os.remove(path)
        return (os.path.basename(path), True)
    
    
    def delete_tree_dir(self, id: int, dir: str) -> (str, str):        
        path = self.get_path_user(id)
        path = os.path.join(path, dir)
        shutil.rmtree(path)
        return (dir, True)
    

    def move_result_tmp_to_model(self, path_model: str, path_tmp: str, start_filename: str):
        for file in os.listdir(path_tmp):
            if file.startswith(start_filename):
                shutil.move(os.path.join(path_tmp, file),
                            os.path.join(path_model, file))
        return 
    
    
    def rename_file_dir(self, id: int, dir: str, newName: str) -> (str, str):        
        path = self.get_path_user(id)
        path = os.path.join(path, dir)
        parent = os.path.dirname(path)
        newPath = parent + newName
        os.rename(path, newPath)
        return(newPath)


    def download_a_file(self, id: int, dir: str) -> (str, str):        
        path = self.get_path_user(id)
        path = os.path.join(path, dir)
        path = os.path.join(self.root_run_dir, path)
        file_name = os.path.basename(path)
        return (path, file_name)
    
    def download_a_dir(self, id: int, dir: str) -> (str, str):        
        path = self.get_path_user(id)
        path = os.path.join(path, dir)
        path = os.path.join(self.root_run_dir, path)
        file_name = os.path.basename(path)
        zip_file_name = file_name + '.zip'
        zip_path = path + '.zip'
        with ZipFile(zip_path, 'w', ) as zip_ref:
            for folder_name, subfolders, filenames in os.walk(path):
                for filename in filenames:
                    file_path = os.path.join(folder_name, filename)
                    zip_ref.write(file_path, arcname=os.path.relpath(file_path, path))
        return (zip_path, zip_file_name)


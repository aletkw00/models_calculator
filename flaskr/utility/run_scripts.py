import subprocess

#python = 'python' # locale con Visual Studio code
python = '/home/donadon/web-server-flask/venv/bin/python3' # nel server

path_RL_models_creator = './script/regression/models_creator.py'
path_delete_file_timer = './script/utility/delete_file_timer.py'

class GenerateRegressionModel:
    def __init__(self, upload_Path: str, result_path_TMP: str) -> None:
        self.command = [
            python,
            path_RL_models_creator,
            upload_Path,
            result_path_TMP
        ]

    def flag_window(self, window):
        window = '-i' + window
        self.command.append(window)

    def flag_filename(self, file_result_name):
        filename = '-o' + file_result_name
        self.command.append(filename)

    def flag_test(self):
        test = '-test'
        self.command.append(test)

    def run_script(self):
        try:
            result = subprocess.run(self.command,
                                    stdout = subprocess.PIPE,
                                    stderr = subprocess.PIPE,
                                    universal_newlines=True)

            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"Error: {result.stderr.strip()}"

        except subprocess.CalledProcessError:
            return 'Something went wrong with the script'
        

class DeleteFileTimer:
    def __init__(self, path_file_to_delete: str) -> None:
        # WAITING TIME BEFORE DELETION
        # IT IS IN SECONDS
        self.time = 15
        #command must be in a single string
        self.command = [python,
            path_delete_file_timer,
            '-file', path_file_to_delete,
            '-time', str(self.time)]
        #print(self.command)
        subprocess.Popen(self.command)


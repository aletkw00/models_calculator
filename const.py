import os

COLONNE_ORE = ['00h', '01h', '02h', '03h', '04h', '05h','06h', '07h', '08h', \
               '09h', '10h', '11h', '12h', '13h', '14h', '15h', '16h', '17h', \
               '18h', '19h', '20h', '21h', '22h', '23h']

COLONNE_GIORNI = ['1d', '2d', '3d', '4d', '5d','6d', '7d', '8d', '9d', '10d', \
                  '11d', '12d', '13d', '14d', '15d', '16d', '17d', '18d', '19d', \
                  '20d', '21d', '22d', '23d', '24d', '25d', '26d', '27d', '28d', \
                  '29d', '30d', '31d']
COLONNE_MESI = ['1m', '2m', '3m', '4m', '5m', '6m', '7m', '8m', '9m', '10m', \
                '11m', '12m']
INPUT_FILE = 'input.csv'
OUTPUT_FILE = 'output.csv'
CSV_DIR = os.path.join('flaskr', 'uploads')
MODEL_DIR = 'dir_of_models'
DEFAULT_MODEL_NAME = 'final'
TMP_MODELS_DIRECTORY = '.tmp_models_dir'
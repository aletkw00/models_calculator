from reg_class import Regression
from utils import *
import argparse
import os
import time

def main(file1, window):
    """Given a file name and a window of previous timestamps,
    use a list of model (already generated) from the json folder,
    to calculate a prediticion row by row from the input file

    Args:
        file1 (str): name of the input file
        window (int): window of the previous timestamps
    """
    inp = csv_read(file1)
    path = 'json_files/'
    inp = add_cols(inp, window)
    for row in range(len(inp)):
        for i in ([name for name in os.listdir('json_files/')]):
            new_path = path + i
            Regr = Regression.json_read(new_path)
            if Regr.window == window:
                print(i, ': ',Regr.predict(inp.iloc[[row]]))
        time.sleep(2)

parser = argparse.ArgumentParser(description='Prediction using multiple model')
parser.add_argument('input', type=str,
                    help='name of the file to get the input')

parser.add_argument('-i', '--window', type=int,
                    help='window')
args = parser.parse_args()

main(args.input, args.window)
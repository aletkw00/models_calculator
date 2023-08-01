from reg import make_regression
from utils import *
import os
import argparse

def model_calc(inp, out, window, test=False):
    """Calculate the model and save it in a json file format.

    Args:
        inp (DataFrame): input DataFrame
        out (DataFrame): output Dataframe
        i (int): counter to save json files
        window (int): window of the previous timestamps
        name (str): name to save the json file
        test (bool): devide data into 80% train and 20% test
    """
    inp, out = alligned(inp, out, window)
    Regr = make_regression(inp, out, window, test)
    return Regr


def main(csv_dir, models_dir, test=False, window=0, name=DEFAULT_MODEL_NAME):
    """Given the path of csv directory and a path to save the models, 
    optionally the other flags, call the function 'model_calc' to 
    calculate a model of the input  files with every output. 
    (The csv direcotry must have one and oly one file as input)

    Args:
        csv_dir (string): path to a directory of csv files
        models_dir (string): path to save the models created
        test (bool): split the data in 80 then do the test.
        window (int): size of the window. Defaults to 0.
        name (string): The names under which to save the created models.
    """
    inp = csv_read(csv_dir + INPUT_FILE)
    for index in range(1, sum(1 for f in os.scandir(csv_dir) if f.is_file())):
        out = csv_read(f"{csv_dir}st{index}_{OUTPUT_FILE}")   
        Regr = model_calc(inp, out, window, test)
        path = os.path.join(models_dir, f"{name}_{str(index)}.json")
        Regr.saveJson(path) 



parser = argparse.ArgumentParser(description='Calculate models')
parser.add_argument('input1', type=str,
                    help='directory of csv')
parser.add_argument('input2', type=str,
                    help='directory of models')
parser.add_argument('-t', '--test',
                    help='devide data files into 80% train and 20% test ')
parser.add_argument('-i', '--window', type=int,
                    help='window of previous timestamps')
parser.add_argument('-o', '--name', type=str,
                    help='output json file name')

args = parser.parse_args()
if args.test and args.name and args.window:
    main(args.input1, args.input2, True, args.window, args.name)
elif args.test and args.window:
    main(args.input1, args.input2, True, args.window)
elif args.test and args.name:
    main(args.input1, args.input2, True, name=args.name)
elif args.window and args.name:
    main(args.input1, args.input2, False, args.window, args.name)
elif args.test:
    main(args.input1, args.input2, True)
elif args.name:
    main(args.input1, args.input2, False, name=args.name)
elif args.window:
    main(args.input1, args.input2, False, args.window)
else:
    main(args.input1, args.input2)
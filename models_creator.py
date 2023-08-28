from reg import make_regression
from utils import *
import os
import argparse

def model_calc(inp, out, window, test=False):
    """Calculate the model.

    Args:
        inp (DataFrame): input DataFrame
        out (DataFrame): output Dataframe
        window (int): window of the previous timestamps
        test (bool): devide data into 80% train and 20% test
    """
    inp, out = alligned(inp, out, window)
    Regr = make_regression(inp, out, window, test)
    return Regr


def get_models(csvDir, finalModelsDir, test=False, window=0, name=DEFAULT_MODEL_NAME):
    """Given the path of csv directory and a path to save the models, 
    optionally the other flags, call the function 'model_calc' to 
    calculate a model based on the input files. This function iterate on output files
    then call that function for each one passing always the same input file.
    (The csv direcotry must have one and only one file as input)

    Args:
        csvDir (string): path to a directory of csv files
        finalModelsDir (string): path to save the models created
        test (bool): split the data in 80 then do the test.
        window (int): size of the window. Defaults to 0.
        name (string): The names under which the created models are to be saved.
    """
    inp = csv_read(csvDir + INPUT_FILE)
    for index in range(1, sum(1 for f in os.scandir(csvDir) if f.is_file() and f.name != '.gitkeep')):
        out = csv_read(f"{csvDir}st{index}_{OUTPUT_FILE}")   
        Model = model_calc(inp, out, window, test)
        path = os.path.join(finalModelsDir, f"{name}_{str(index)}.json")
        Model.saveJson(path) 



parser = argparse.ArgumentParser(description='Calculate models')
parser.add_argument('csvDir', type=str,
                    help='directory of csv')
parser.add_argument('finalModelsDir', type=str,
                    help='directory of models')
parser.add_argument('-t', '--test',
                    help='devide data files into 80% train and 20% test ')
parser.add_argument('-i', '--window', type=int,
                    help='window of previous timestamps')
parser.add_argument('-o', '--name', type=str,
                    help='output json file name')

args = parser.parse_args()
if args.test and args.name and args.window:
    get_models(args.csvDir, args.finalModelsDir, True, args.window, args.name)
elif args.test and args.window:
    get_models(args.csvDir, args.finalModelsDir, True, args.window)
elif args.test and args.name:
    get_models(args.csvDir, args.finalModelsDir, True, name=args.name)
elif args.window and args.name:
    get_models(args.csvDir, args.finalModelsDir, False, args.window, args.name)
elif args.test:
    get_models(args.csvDir, args.finalModelsDir, True)
elif args.name:
    get_models(args.csvDir, args.finalModelsDir, False, name=args.name)
elif args.window:
    get_models(args.csvDir, args.finalModelsDir, False, args.window)
else:
    get_models(args.csvDir, args.finalModelsDir)
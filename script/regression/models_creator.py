import argparse
import os

from reg import make_regression
from utils import alligned, csv_read
from const import DEFAULT_MODEL_NAME, INPUT_FILE

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

    output_files = sorted([os.path.join(csvDir,f.name) for f in os.scandir(csvDir) if f.is_file() and f.name != INPUT_FILE and f.name != '.keep'])

    output = csv_read(output_files)
    inp = csv_read(os.path.join(csvDir,INPUT_FILE))
    if inp is None:
        raise Exception("RottoTuttoException: "+os.path.join(csvDir,INPUT_FILE))
    
    index = 1
    
    for out in output:  
        Model = model_calc(inp, out, window, test)
        path = os.path.join(finalModelsDir, f"{name}_{str(index)}.json")
        Model.saveJson(path) 
        index+=1


def def_parser_args():
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
    return parser


if __name__ == "__main__":
    parser = def_parser_args()
    ARGS = parser.parse_args()
    if ARGS.test and ARGS.name and ARGS.window:
        get_models(ARGS.csvDir, ARGS.finalModelsDir, True, ARGS.window, ARGS.name)
    elif ARGS.test and ARGS.window:
        get_models(ARGS.csvDir, ARGS.finalModelsDir, True, ARGS.window)
    elif ARGS.test and ARGS.name:
        get_models(ARGS.csvDir, ARGS.finalModelsDir, True, name=ARGS.name)
    elif ARGS.window and ARGS.name:
        get_models(ARGS.csvDir, ARGS.finalModelsDir, False, ARGS.window, ARGS.name)
    elif ARGS.test:
        get_models(ARGS.csvDir, ARGS.finalModelsDir, True)
    elif ARGS.name:
        get_models(ARGS.csvDir, ARGS.finalModelsDir, False, name=ARGS.name)
    elif ARGS.window:
        get_models(ARGS.csvDir, ARGS.finalModelsDir, False, ARGS.window)
    else:
        get_models(ARGS.csvDir, ARGS.finalModelsDir)
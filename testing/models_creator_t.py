from reg import make_regression
from utils import *
import argparse
from timeit import default_timer as timer

def model_calc(inp, out, i, window, name, test=False):
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
    start = timer()
    Regr = make_regression(inp, out, window, test)
    end = timer()
    print(end - start)
    path = MODEL_DIR + 'Nuovo/'+name+str(i)+'.json'
    Regr.saveJson(path)


def main(lista, test=False, window=0, name='final-'):
    """Given a list of file name and optionally the other flags,
    use the first file of the list as input file and the rest as output,
    then call the function 'model_calc' to calculate a model of the input with
    every output.

    Args:
        lista (list): list of file name
        test (bool): devide data into 80% train and 20% test. Defaults to False.
        window (int): window of the previous timestamps. Defaults to 0.
        name (str): name to save the json file. Defaults to 'final-'
    """

    inp = csv_read(lista[0])
    output = csv_read(lista[1:])
    i = 1
    for out in output:
        model_calc(inp, out, i, window, name, test)
        i += 1

parser = argparse.ArgumentParser(description='Calculate models')
parser.add_argument('input', type=str, nargs='+',
                    help='first file must be the input file and next to it \
                        there must be a list of output file')
parser.add_argument('-t', '--test',
                    help='devide data files into 80% train and 20% test ')
parser.add_argument('-i', '--window', type=int,
                    help='window of previous timestamps')
parser.add_argument('-o', '--name', type=str,
                    help='output json file name')

args = parser.parse_args()
if args.test and args.name:
    main(args.input, True, args.window, args.name)
elif args.test:
    main(args.input, True, args.window)
elif args.name:
    main(args.input, False, args.window, name=args.name)
else:
    main(args.input)
from reg import make_regression
from utils import *
import pandas as pd
import json

"""
inp = csv_read('Useful_Data/Input.csv')
#inp = csv_read(['csv_files/1.csv', 'csv_files/2.csv', 'csv_files/3.csv'])

inp = merging(inp)
out = csv_read('Useful_Data/output_1.csv')

inp, out = alligned(inp, out, 0)


Regr = make_regression(inp, out, test=True)
Regr.saveJson('json_files/final-4.json')

"""

df = pd.DataFrame({'angles': [0, 3, 4],
                   'degrees': [360, 180, 360]},
                  )
df1 = pd.DataFrame({'degrees': [360, 180, 360],
                    'angles': [0, 3, 4]},
                  )
df = add_cols(df, -1)
print(df)
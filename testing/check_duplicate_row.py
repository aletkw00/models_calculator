import os
import pandas as pd
import datetime 

file1 = 'dati.csv'
path = 'csv_files/Old_and_test/' + file1

#correct_path = 'csv_files/Correct/'+file1


df = pd.read_csv(path, low_memory=False)
"""
if df.iloc[0, 0].find('/') >= 0:
            if len(df.iloc[0,0])>18:
                df[df.columns[0]] = pd.to_datetime(df[df.columns[0]], format='%d/%m/%Y %H:%M:%S')
            else:
                df[df.columns[0]] = pd.to_datetime(df[df.columns[0]], format='%d/%m/%Y %H:%M')
        else:
            df[df.columns[0]] = pd.to_datetime(df[df.columns[0]], format='%Y-%m-%d %H:%M:%S')

"""
df[df.columns[0]] = pd.to_datetime(df[df.columns[0]], infer_datetime_format=True, errors='coerce')
df = df.sort_values(df.columns[0])
df.to_csv('bello.csv')

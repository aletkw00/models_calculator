import pandas as pd
import numpy as np
from const import *
import datetime

def process_dataframe(df):
    df.rename(columns={df.columns[0]: "timestamps"}, inplace=True)
    
    df[df.columns[0]] = pd.to_datetime(df[df.columns[0]], infer_datetime_format=True, errors='coerce')

    df.drop([col for col in df.columns if col != df.columns[0] and \
                (not df[col].dtype == float and not df[col].dtype == int)], \
            axis=1, inplace=True)
    
    df.dropna(inplace=True)
    df.drop_duplicates(subset=df.columns[0], inplace=True)
    df.reset_index(drop=True, inplace=True)

def csv_read(inp):
    """
    Take a CSV file and convert it into a DataFrame. Remove columns that have 
    non-numeric values, except for the timestamps column. 
    Drop rows that have at least one NaN value. 
    Lastly, remove any duplicate rows from the DataFrame.

    Args:
        inp (str or list): Name of the file or list of file names.

    Returns:
        DataFrame or list of DataFrames.
    """
        
    try:
        if isinstance(inp, str):
            df = pd.read_csv(inp, sep=',')
            process_dataframe(df)
            return df
        
        elif isinstance(inp, list):
            dataframes = [pd.read_csv(filename) for filename in inp]
            for df in dataframes:
                process_dataframe(df)
            return dataframes
        
        else:
            raise ValueError("Please enter a CSV file list or a CSV file name.")
    
    except:
        print("Files are not well formatted. Make sure the first column of every file is a timestamp column"
              "with one of the two allowed formats:\n"
              "1) %d/%m/%Y %H:%M:%S   --> 18/12/2000 20:00:00\n"
              "2) %Y-%m-%d %H:%M:%S   --> 2000-12-20 20:00:00")
        


def merging(inp, name: str = ''):
    """Given a list of DataFrames, this function crosschecks the timestamps
    to find rows that are present in every DataFrame of the list. It then 
    creates an output DataFrame with all the common rows and combines the 
    columns from each DataFrame.

    Args:
        inp (DataFrame): list of DataFrames
        name (str): name of the file where to save the result

    Returns:
        DataFrame: A DataFrame that contains rows common to all DataFrames
    """
    if isinstance(inp, list):

        start_df = inp[0]
        # Merge all DataFrames based on the timestamp column
        for df in inp[1:]:
            # Find columns that are repeated in both DataFrames
            double = [col for col in df.columns if col in start_df.columns \
                      and col != df[df.columns[0]]]
           
            # Drop one of the repeated columns
            df = df.drop(double, axis=1)
            
            # Merge the two DataFrames
            start_df = pd.merge(start_df, df, on=start_df.columns[0])

        # Reset the index
        start_df = start_df.reset_index(drop=True)
        
        # Save the DataFrame as a CSV file if a name is provided
        if name != '':
            start_df.to_csv(name, index=None)
        return start_df 
    
    else:
        return inp

def get_time(dfc):
    """Manipulate timestamps to obtain a DataFrame weighted on month-day-hour
    (MxDxH).
    The input dataframe must have first column as timestamp column
    
    Args:
        df (DataFrame): a DataFrame with the first column as timestamp

    Returns:
        DataFrame: the passed DataFrame with the MxDxH matrix instead of
            the timestamp column
    
    """
    # Create a copy of the DataFrame
    df = dfc.copy()

    # Convert the first column in datetime if it is not 
    if not isinstance(df.iloc[0,0], datetime.datetime):
        df[df.columns[0]] = pd.to_datetime(df[df.columns[0]], infer_datetime_format=True, errors='coerce')

    # Split the timestamp column in 3 different columns: month, day, hour
    df['month'] = df[df.columns[0]].dt.month
    df['day'] = df[df.columns[0]].dt.day
    df['hour'] = df[df.columns[0]].dt.strftime('%H')
    
    # Create and populate the DataFrame of the Hour
    i=0
    dfH = pd.DataFrame(0, index=np.arange(df.shape[0]), columns=COLONNE_ORE)    
    for ora in df['hour']:           
        dfH.at[i, ora+'h'] = 1
        i+=1

    # Create and populate the DataFrame of the Day
    i=0
    dfD = pd.DataFrame(0, index=np.arange(df.shape[0]), columns=COLONNE_GIORNI)  
    for giorno in df['day']:
        dfD.at[i, str(giorno)+'d'] = 1 
        i+=1

    # Create and populate the DataFrame of the Month
    i=0
    dfM = pd.DataFrame(0, index=np.arange(df.shape[0]), columns=COLONNE_MESI)    
    for mese in df['month']:
        dfM.at[i, str(mese)+'m'] = 1 
        i+=1
    # Drop of the previously created columns and timestamp column
    df = df.drop([df.columns[0], 'day', 'hour', 'month'], axis=1)

    # Create the MxDxH DataFrame
    df1 = pd.concat([dfM, dfD, dfH], axis=1)

    if(len(df) == 1):
        df = df.reset_index(drop=True)

    df = pd.concat([df1, df], axis=1)
    return df

def add_col(df, i):
    """"Given a DataFrame, this function returns a new DataFrame containing 
    only the previous 'i' rows from the original DataFrame. The columns in the 
    new DataFrame are named 'col-i', indicating the number of rows before 
    the current row.
    """
    #create a dataframe which has from col 1 to the end and the first n-i rows
    df1 = df.iloc[0:len(df)-i, 1:]
    #changing the col names for the new dataframes
    suffix='-'+str(i)
    df1 = df1.add_suffix(suffix)
    #reset the row index
    df1.index = df1.index + i    
    return df1
    
def add_cols(df, i: int):
    """Given a DataFrame, this function returns a new DataFrame where
      each row is concatenated with the previous 'i' rows. 
      The first 'i' rows are eliminated because they do not contain 
      all the necessary previous 'i' row values.

    """
    #if window is 0 then return the passed Dataframe
    if i==0:
        return df
    elif i >= len(df):
        raise ValueError("There aren't enough rows for this size of window")        
    elif i < 0:
        raise ValueError("the window must be a positive integer") 
    
    dataframe_list= list()
    dataframe_list.append(df)
    for n in range(1,i+1):
        df1 = add_col(df, n)
        dataframe_list.append(df1)

    df = pd.concat(dataframe_list, axis=1)
    df = df.iloc[i:]
    df = df.reset_index(drop=True)
    return df



def alligned(inp, output, window: int):
    """Make sure the outputs will be alligned for timestamp column

    Args:
        inp (DataFrame): a DataFrame with the first column as timestamp
        output (DataFrame): a DataFrame with the first column as timestamp
        window (int): size of the window

    Returns:
        DataFrame: a DataFrame with the first column as timestamp
        DataFrame: a DataFrame with the first column as timestamp
    """
    # Adding the window table
    try:
        inp = add_cols(inp, window)
    except ValueError as e:
        print(e)

    # Check if a timestamp of one DataFrame is in the other
    # If not drop the row
    inp = inp[inp[inp.columns[0]].isin(output[output.columns[0]])]
    output = output[output[output.columns[0]].isin(inp[inp.columns[0]])]
    
    # Sort the DataFrames by timestamps
    inp = inp.sort_values(inp.columns[0])
    output = output.sort_values(output.columns[0])

    # Index reset
    inp = inp.reset_index(drop=True)
    output = output.reset_index(drop=True)
    
    return inp, output



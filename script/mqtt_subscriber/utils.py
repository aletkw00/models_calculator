import pandas as pd

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

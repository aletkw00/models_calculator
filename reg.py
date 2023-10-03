import pandas as pd
import numpy as np
import statsmodels.api as sm
from stepwise_regression import step_reg
from reg_class import RegressionModel
import math
from const import *
from utils import get_time

def get_normalize(df):
    """return the the passsed Dataframe normalized
    """
    return (df-df.mean())/df.std()


def make_regression(X_train, Y_train, window: int, test: bool=True):
    """Calculate a linear regression model starting with 2 DataFrames.
    The models are computed through step-wise regression procedures.

    Args:
        X_train (DataFrame)
        Y_train (DataFrame)
        window (int)
        test (bool): if True divides the data in 80% train and 20% test. 
            
    Returns:
        Regression: object of class Regr wich contanins:
            Series: a coefficent vector of the linear regression
            Series: a mean vector of every column of inp_train
            Series: a standard deviation vector of every column of inp_train
            float: out_train mean
            float: out_train standard deviation
            list: the list of columns not used
            window: the number of previous timestamps to consider

    """
    if test:
        # Divide the two DataFrames into 80% train and 20% test
        X_test = X_train.iloc[(len(X_train.index) // 100) * 60:\
                              (len(X_train.index) // 100) * 80, :]
        
        X_train = pd.concat([
            X_train.iloc[:(len(X_train.index) // 100) * 60, :],
            X_train.iloc[(len(X_train.index) // 100) * 80:, :]  
        ])

        Y_test = Y_train.iloc[(len(Y_train.index) // 100) * 60:\
                              (len(Y_train.index) // 100) * 80, :]
        
        Y_train = pd.concat([
            Y_train.iloc[:(len(Y_train.index) // 100) * 60, :],
            Y_train.iloc[(len(Y_train.index) // 100) * 80:, :]
        ])
        
        # Reset all DataFrame indices
        X_test = X_test.reset_index(drop=True)
        Y_test = Y_test.reset_index(drop=True)
        X_train = X_train.reset_index(drop=True)
        Y_train = Y_train.reset_index(drop=True)
    
    #TRAIN
    X_train = get_time(X_train)
    input_calibrazione = X_train
    output_calibrazione = Y_train.iloc[:, -1]

    # Save the mean and standard deviation of input_calibrazione
    calib_inp_media = input_calibrazione.mean()
    calib_inp_stdev = input_calibrazione.std()
    
    # Get the list of columns which would return NaN during normalization 
    # and then drop those columns
    unselected_columns = list()
    for idx, j in calib_inp_stdev.items():
        #if the value of the idx items of list is equal to 0
        if j==0:
            unselected_columns.append(idx)
            input_calibrazione = input_calibrazione.drop(idx, axis=1)
            #set the value of the item from 0 to 1
            calib_inp_stdev.at[idx] = 1
    if unselected_columns:
        print('\n\nMissing values in: ')
        print(unselected_columns)

    # Save the mean and standard deviation of output_calibrazione
    calib_output_media = output_calibrazione.mean()
    calib_output_stdev = output_calibrazione.std()

    # Get the normalization of input_calibrazione and output_calibrazione
    norm_calib_inp = get_normalize(input_calibrazione)
    norm_calib_out = get_normalize(output_calibrazione)

    # Step forward
    fwdselect = step_reg.forward_regression(norm_calib_inp, \
                                            norm_calib_out, \
                                            0.0001, \
                                            verbose=False)
    
    # Step backward
    backselect = step_reg.backward_regression(norm_calib_inp.loc[:, fwdselect], \
                                              norm_calib_out, \
                                              0.0001, \
                                              verbose=False)
    
    # Filter columns selected by forward and backward selection
    selected_columns = [col for col in norm_calib_inp.columns if col in backselect]

    # Remove timestamp columns
    selected_columns = [col for col in selected_columns if 
                            col not in COLONNE_ORE and 
                            col not in COLONNE_GIORNI and 
                            col not in COLONNE_MESI]
    
    
    # Reintroduce all columns of MxDxH with values
    norm_calib_inp = pd.concat([norm_calib_inp.loc[:, :COLONNE_ORE[-1]], \
                                norm_calib_inp[selected_columns]], axis=1)
    #
    #
    #
    #Elimino le colonne dei timestamp
    #norm_calib_inp = tmp_inp_cal
    #
    #
    #
    #adding to the list the column not selceted
    [unselected_columns.append(col) for col in X_train.columns \
     if col not in unselected_columns and col not in norm_calib_inp]
    
    #MODEL CREATION

    # add a constant 
    norm_calib_inp = sm.add_constant(norm_calib_inp)
    # define the model and fit it
    model = sm.OLS(norm_calib_out, norm_calib_inp)
    results = model.fit()


    # CREATE A COEFFICIENT MASK OF THE ORIGINAL DATAFRAME
    # Get the coefficients from the model results as numpy array    
    B = results.params
    
    # Initialize coefficient mask with zeros (coeff + X_train.columns)
    B_f= [0] * (len(X_train.columns) + 1)
    
    # Get the column indices of the selected coefficients (+1 to compensate the const coefficent)
    norm_calib_inp_indx = [0] # const coefficient is not in X_train columns
    norm_calib_inp_indx.extend([X_train.columns.get_loc(col) + 1 
                                for col in norm_calib_inp.columns 
                                    if col != 'const'])
    
    #save the coefficent values in the mask
    cont = 0
    for i in norm_calib_inp_indx:
        B_f[i] = B.values[cont]
        cont+=1

    # Convert the coefficient mask to a pandas Series
    B_f = pd.Series(B_f)

    # Obtain the denormalized predictions for the calibration set
    final_normy = pd.Series(np.dot(norm_calib_inp, B))
    final_deny = (final_normy*calib_output_stdev)+calib_output_media
    
    #calculation and printing of approximation errors
    TSS_train = sum((output_calibrazione-final_deny)**2)
    RSS_train = sum((output_calibrazione-calib_output_media)**2)
    AdjR2 = 1 - (((len(output_calibrazione)-1)/(len(output_calibrazione)-\
                            len(norm_calib_inp.columns)-2))*\
                            (TSS_train/RSS_train))
    BMSEadj = math.sqrt(sum((output_calibrazione-final_deny)**2)/\
                        sum(output_calibrazione**2))
    RRSE = math.sqrt((sum((output_calibrazione-final_deny)**2)/\
                      sum((output_calibrazione-calib_output_media)**2)))
    print(f'\nAdjR2 del modello:  {AdjR2:.4f} \n'
          f'BMSEadj del modello: {BMSEadj:.4f} \n'
          f'RRSE del modello: {RRSE:.4f}')
    
    #TEST
    if test:
        X_test = get_time(X_test)
        inp_validazione = X_test
        out_validazione = Y_test.iloc[:, -1]
        
        #normalize
        norm_valid_inp = (inp_validazione - calib_inp_media) / calib_inp_stdev
        #add a constant 
        norm_valid_inp = sm.add_constant(norm_valid_inp, has_constant='add')
        #get the normalize Dataframe    
        check = pd.Series(np.dot(norm_valid_inp, B_f))
        #get the denormalized DAtaFrame
        deny_test = (check*calib_output_stdev)+calib_output_media
        #calculation and printing of approximation errors
        TSS_test = sum((out_validazione-deny_test)**2)
        RSS_test = sum((out_validazione-calib_output_media)**2)
        AdjR2_test = 1 - (((len(out_validazione)-1)/\
                           (len(out_validazione)-\
                            len(norm_valid_inp.columns)-2))*\
                           (TSS_test / RSS_test))
        MAPE = np.mean(np.abs(out_validazione-deny_test)/out_validazione, axis=0)
        print('\nAdjR2_test:', AdjR2_test, '\nR2:', (1-(TSS_test / RSS_test)), '\nMAPE:', MAPE)
        
    B_f.index = ['const'] + X_train.columns.to_list()

    return RegressionModel(B_f, calib_inp_media, calib_inp_stdev, \
                      calib_output_media, calib_output_stdev, unselected_columns, \
                      window)
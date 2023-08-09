import json
import pandas as pd
import numpy as np
import statsmodels.api as sm
from utils import get_time

class RegressionModel:
    """collect all the model attributes

    Attributes:
        B (str): This is where we store arg,
        calib_input_media (Series): mean of each column of the input DataFrame
        calib_input_stdev (Series): standard dev of each column of the input DataFrame
        calib_output_media (float): mean of the output values
        calib_output_stdev (float): standard deviation of output values
        unselected_columns (list): list of columns not used in the model
        window (int): the number of previous timestamps to consider
    """

    def __init__(self, B, calib_input_media, calib_input_stdev, \
                 calib_output_media, calib_output_stdev, unselected_columns, \
                    window):
        self.B = B
        self.calib_inp_media = calib_input_media
        self.calib_inp_stdev = calib_input_stdev
        self.calib_out_media = calib_output_media
        self.calib_out_stdev = calib_output_stdev
        self.unselected_columns = unselected_columns
        self.window = window

    def __str__(self): 
        
        return f"Matrice di coefficenti B:\n{self.B}\
             \n\nmedia di X:\n{self.calib_inp_media}\
             \n\ndeviazione standard X:\n{self.calib_inp_stdev}\
             \n\nmedia di Y:\n{self.calib_out_media:.4f}\
             \n\ndeviazione standard Y:\n{self.calib_out_stdev:.4f}\
             \n\ncolonne non selezionate:\n{self.unselected_columns}\
             \n\nwindow:\n{self.window}"

    
    def saveJson(self, name='data.json'):
        """save the class object in a json file

        Args:
            name (str): name of file json. Defaults to 'data.json'
        """
        obj_dict = {
            'B': self.B.to_dict(),
            'calib_input_media': self.calib_inp_media.to_dict(),
            'calib_input_stdev': self.calib_inp_stdev.to_dict(),
            'calib_output_media': float(self.calib_out_media),
            'calib_output_stdev': float(self.calib_out_stdev),
            'unselected_columns': self.unselected_columns,
            'window': self.window
        }
        
        with open(name, 'w', encoding='utf-8') as f:
            json.dump(obj_dict, f, ensure_ascii=False, indent=4)


    def predict(self, input_valid):
        """
        Use a previously created model to get a prediction for the input.

        Args:
            input_valid (DataFrame): Input DataFrame.
        Returns:
            float: The prediction result.
        """
        input_valid = get_time(input_valid)
        lista = list(self.B.keys())

        lista.pop(0)
        input_valid.columns = lista

        # Normalize input
        norm_valid_inp = (input_valid-self.calib_inp_media)/self.calib_inp_stdev

        # Add a constant
        norm_valid_inp = sm.add_constant(norm_valid_inp, has_constant='add')

        # Get the normalize Dataframe    
        final_normy = pd.Series(np.dot(norm_valid_inp, self.B))

        # Get the denormalized DataFrame
        final_deny = (final_normy*self.calib_out_stdev)+self.calib_out_media
        
        return final_deny[0]
        


    def json_read(name):
        """given a json file name returns an object of class Regression
        reading data from the file.

        Args:
            name (str): json file name

        Returns:
            Regression: object of class Regr wich contanins:
                Series: coefficent vector of the linear regression
                Series: mean vector of every column of inp_train
                Series: standard deviation vector of every column of inp_train
                float: out_train mean
                float: out_train standard deviation
                list: the list of columns not used
                int: the number of previous timestamps to consider

        """
        data = json.load(open(name))
        Model = Model(pd.Series(data[list(data.keys())[0]]), \
                          pd.Series(data[list(data.keys())[1]]), \
                          pd.Series(data[list(data.keys())[2]]), \
                          data[list(data.keys())[3]], \
                          data[list(data.keys())[4]], \
                          data[list(data.keys())[5]], \
                          data[list(data.keys())[6]])

        return Model

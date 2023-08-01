import pandas as pd

 
def make_regression(X_train, Y_train, window, test=True):

    #devide the two Dataframe into 80% train and 20% test  (60-20-20)
    X_test = X_train.iloc[(len(X_train.index)//100)*60:\
                                (len(X_train.index)//100)*80, :]
    X_train = pd.concat([X_train.iloc[:(len(X_train.index)//100)*60, :],\
                            X_train.iloc[(len(X_train.index)//100)*80:, :]])

    Y_test = Y_train.iloc[(len(Y_train.index)//100)*60:\
                                (len(Y_train.index)//100)*80, :]
    Y_train = pd.concat([Y_train.iloc[:(len(Y_train.index)//100)*60, :],\
                            Y_train.iloc[(len(Y_train.index)//100)*80:, :]])


    
    #devide the two Dataframe into 80% train and 20% test  (80-20)
    X_test = X_train.iloc[(len(X_train.index)//100)*80:, :]
    X_train = X_train.iloc[:(len(X_train.index)//100)*80, :]

    Y_test = Y_train.iloc[(len(Y_train.index)//100)*80:, :]
    Y_train = Y_train.iloc[:(len(Y_train.index)//100)*80, :]

    #reset all DataFrame indexs
    X_test = X_test.reset_index(drop=True)
    Y_test = Y_test.reset_index(drop=True)
    X_train = X_train.reset_index(drop=True)
    Y_train = Y_train.reset_index(drop=True)
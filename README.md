# Simple Guide to use the library

## Dependencies:
- ipaddress
- shutil
- Flask
- paho-mqtt
- pandas
- numpy
- statsmodels
- stepwise-regression


## Input files formatting

- file must be a csv file and has to be separeted by ",".
- file must have a header
- first column has to be the timestamps column

## Usage
>Run `app.py`, which is the server application. A user can connect to the server by using an IP address and create their own models by providing an input file and output files (in addition to other flags for customizing the models). Once the models are created, the user can decide to save or delete them. All saved models will be stored in the user's directory. Users can also associate a custom broker with the models by defining it in the appropriate section.

### models_creator.py
This script is run by app.py and takes the following inputs:

 - A path to a directory that contains all the CSV files to be used for creating the models. One file is for input, and the rest are for output.
 - A path to a directory where all the created models will be saved.
 - (Optional) A flag to split the data, using 80% as training data and the other 20% as test data.
 - (Optional) A flag to make the data dependent on the 'i' previous timestamps. Default value is 0.
 - (Optional) A string to rename the final model, which will be saved as a JSON file. Default is 'final-.json'.

This script will create the same number of models as the number of output files passed to the script.


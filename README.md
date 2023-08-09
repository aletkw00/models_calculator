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
>Run `run.py`, which launches the server application. A user can connect to the server by using an IP address and create their own models by providing those parameters:

    - The name of directory to models to create (if not already existent then will be created)
    - An input file of csv type
    - At least one output file of csv type
    - An integer value for the window
    - A name for the model to create
    - A flag to split data in 80% test and 20% test. (if true then will be showed some check of the created model)

The server will create the same number of models as the number of output files passed to it.
Once the model is created, the user can decide to save or delete it. All saved models will be stored in the user's directory. Users can also associate a custom broker with the models by defining it in the appropriate section.



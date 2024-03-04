#!/bin/bash
python -m venv venv
./venv/Script/activate
echo install requirements depends on python version
echo -----------
echo for python 3.11
echo python -m pip install -r requirements-base.txt
echo -----------
echo for python 3.6 
echo python -m pip install -r requirements-python36.txt
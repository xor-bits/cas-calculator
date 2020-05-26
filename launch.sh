#!/bin/bash

# install
python -m venv __venv__
source __venv__/bin/activate

# update
pip install -r requirements.txt

# run
python main.py
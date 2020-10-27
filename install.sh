#!/bin/bash

# venv
python -m venv __venv__
source __venv__/bin/activate

# update
pip install -r requirements.txt
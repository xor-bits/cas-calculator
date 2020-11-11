#!/bin/bash
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

# venv
python3 -m venv __venv__
source __venv__/bin/activate

# update
pip3 install -r requirements.txt

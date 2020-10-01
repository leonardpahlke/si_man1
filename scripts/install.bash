#!/usr/bin/env bash
# create virtual environment if not found
if [[ ! -d venv ]]; then
  echo create python3.8 virtual environment
  python3.8 -m venv venv
  echo activating new virtual environment
fi
source venv/bin/activate
# install project dependencies
pip install -r requirements.txt

# set module to PYTHONPATH
export PYTHONPATH=$(pwd)
# cd mandatory1 || exit

echo $PYTHONPATH
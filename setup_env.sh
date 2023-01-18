#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r dev-requirements.txt
pip install -r requirements-test.txt
python setup.py install || echo "Failed setup install"
python setup.py test || echo "Failed setup test"
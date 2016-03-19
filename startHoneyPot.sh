#!/bin/bash
export PYTHONPATH=${PYTHONPATH}:$PWD/honeypot/src/main
echo $PYTHONPATH

# To run with authbind, make sure RECCE7_AUTHBIND environment
# variable is set prior to running this script.
$RECCE7_AUTHBIND python3 $PWD/honeypot/src/main/main.py

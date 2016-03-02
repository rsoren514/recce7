#!/bin/bash
export PYTHONPATH=${PYTHONPATH}:$PWD/honeypot/src/main
echo $PYTHONPATH
python3 $PWD/honeypot/src/main/main.py

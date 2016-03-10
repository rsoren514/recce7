#!/bin/bash
export PYTHONPATH=${PYTHONPATH}:$PWD/webserver/src/main
echo $PYTHONPATH
python3 $PWD/webserver/src/main/server/main.py

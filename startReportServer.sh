#!/bin/bash
export PYTHONPATH=${PYTHONPATH}:$PWD/reportserver/src/main
echo $PYTHONPATH
python3 $PWD/reportserver/src/main/server/main.py

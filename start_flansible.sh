#!/bin/bash

FLANSIBLE_DIR={{flansible_dir}}
FLANSIBLEFE_DIR={{flansiblefe_dir}}
ANACONDA_DIR={{anaconda_basedir}}
cd $FLANSIBLE_DIR
export PATH="$ANACONDA_DIR/bin:$PATH"
source activate py27
screen -dmS Celery celery worker -A flansible.celery --loglevel=info
screen -dmS Flansible python runserver.py
screen -dmS Flower flower --broker=redis://localhost:6379/0

cd $FLANSIBLEFE_DIR
screen -dmS FlansibleFE python run.py

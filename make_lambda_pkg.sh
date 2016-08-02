#!/bin/bash

DIR_HOME=$(pwd)
ENV_HOME=$DIR_HOME/venv/lib/python2.7/site-packages
ZIPFILE=$DIR_HOME/lambda_elblog_to_es.zip

zip $ZIPFILE -9 lambda_function.py 
cd $ENV_HOME
zip -g -9r $ZIPFILE *
cd $DIR_HOME

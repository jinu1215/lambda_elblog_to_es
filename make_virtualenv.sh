#!/bin/bash

if [ -d venv ]; then
	echo "virtualenv already exist"
else
	virtualenv --no-site-packages venv
fi

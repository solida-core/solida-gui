#!/bin/bash

#solida info
python solida-gui/manage.py migrate --noinput
python solida-gui/manage.py runserver 0.0.0.0:8000
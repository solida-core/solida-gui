#!/bin/bash

#solida info
python solidagui/manage.py migrate --noinput
python solidagui/manage.py runserver 0.0.0.0:8000
#!/bin/bash

#solida info
python solidagui/manage.py migrate
python solidagui/manage.py runserver 0.0.0.0:8000
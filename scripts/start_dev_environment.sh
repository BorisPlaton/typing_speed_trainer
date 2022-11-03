#!/bin/sh

docker-compose --env-file=.env.dev -f docker-compose.dev.yml up -d "$@"
sleep 1
python typing_speed_trainer/manage.py migrate
python typing_speed_trainer/manage.py runserver 127.0.0.1:8000

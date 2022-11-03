#!/bin/sh

docker-compose -f docker-compose.dev.yml down "$@"
kill $(ps -a | grep -w "python" | grep -oE "\s[0-9]+\s")

#!/bin/sh

docker-compose --env-file=./env/.env.dist -f docker-compose.dev.yml up -d "$@"

#!/bin/bash
#
# Stops all containers that are in the docker-compose.dev.yml file. The
# script will use environment variables from the .env.dist file.

ENV_FILE='env/.env.dist'
DOCKER_FILE='docker-compose.dev.yml'
CURRENT_DIR=$(pwd)

function exit_if_file_not_exists() {
  if ! [[ -f $1 ]]; then
    echo "${1} doesn't exist in the ${CURRENT_DIR}."
    exit 1
  fi
}

exit_if_file_not_exists $ENV_FILE
exit_if_file_not_exists $DOCKER_FILE

if docker-compose --env-file="$ENV_FILE" -f "$DOCKER_FILE" down "$@"; then
  echo -e "\033[1;32mSuccess\033[0m"
else
  echo -e "\033[1;31mFailure\033[0m"
fi

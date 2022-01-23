#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PROJ_DIR=$( dirname "$SCRIPT_DIR")

echo "Building todo project container"
cd $PROJ_DIR
docker build -t todoproject .

echo "Running todo project"
docker run -d --name todo --env-file dockerenv todoproject
docker logs todo
echo "End of todo project"

echo "Removing todo project container"
docker rm todo

echo "Program ran successfully."
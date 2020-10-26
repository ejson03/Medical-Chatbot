#!/bin/bash
docker rmi --force $(docker images)
docker container rm --force $(docker container ls -aq)
docker system prune -a

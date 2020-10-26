#!/bin/bash
docker container rm --force $(docker container ls -aq)
docker rmi --force $(docker images)
docker system prune -a -f
docker volume prune -f

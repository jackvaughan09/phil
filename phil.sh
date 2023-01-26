#!/bin/bash
docker build -t phil .
docker run --name philapp phil
docker cp philapp:app/data extracted
docker container rm -f philapp
docker image rm -f phil
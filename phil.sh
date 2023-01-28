#!/bin/bash
#creates these folders if they don't just in case.
if [ ! -d "data/pdf" ]; then
  mkdir -p "data/pdf"
fi

if [ ! -d "data/zip" ]; then
  mkdir -p "data/zip"
fi
docker build -t phil .
docker run --name philapp phil
docker cp philapp:app/data extracted
docker container rm -f philapp
docker image rm -f phil
# This Dockerfile is only for building the phil base image 
# Command for ARM64 systems: 
# docker build -t jackvaughan/phil:arm64 -f imagebuilder.Dockerfile .
# 
# x64:
# To rebuild the phil:x64 tag, uncomment the LABEL and make sure you tag
# it appropriately (jackvaughan/phil:x64) if you plan on pushing
# docker build -t jackvaughan/phil:x64 -f imagebuilder.Dockerfile .

FROM ubuntu:22.04

#LABEL org.opencontainers.image.platform=linux/amd64
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get -y upgrade && \
    apt-get -y install python3 && \
    apt-get -y install python3-venv && \
    apt-get -y install python3-tk && \
    apt update && apt install python3-pip -y && \
    apt-get install -y bash make ghostscript && \
    apt-get install -y default-jre default-jdk
# Method1 - installing LibreOffice and java
RUN  apt-get --no-install-recommends install libreoffice -y
RUN  apt-get install -y libreoffice-java-common

ARG CACHEBUST=1

# Create the application directory
RUN mkdir -p /app

# Copy the application code and files to scrape
COPY control /app/control
# COPY data /app/data

# Set WD
WORKDIR /app/control

RUN make setup 
RUN chmod +x run.sh
# RUN sh run.sh
FROM python:3.8-buster

RUN apt-get update && apt-get install -y bash make libreoffice ghostscript

# Create the application directory
RUN mkdir -p /app

# Copy the application code and files to scrape
COPY control /app/control
COPY data /app/data

# Set WD
WORKDIR /app/control

# Create venv and install dependencies
RUN make setup

# Run!
# RUN make run

# Need to copy files from container back to 
# host machine.
#RUN docker cp phil :app/data ../data






 




FROM jackvaughan/phil:latest
COPY data /app/data
# Set WD
WORKDIR /app/control
RUN sh run.sh


FROM python:3.10.12-slim

# Set the current working directory to usr/aa-Vector-DBs.
# This is where we'll put the requirements-dev.txt file and the app directory.
WORKDIR /usr/aa-Vector-DBs

# Copy all application files to the container
COPY . /usr/aa-Vector-DBs

# install system dependencies
RUN apt-get update \
  && apt-get -y install make git \
  && apt-get clean

# install python dependencies
RUN make install-dev

# Keep the container running for interactive use
CMD ["tail", "-f", "/dev/null"]

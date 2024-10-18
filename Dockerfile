FROM python:3.10.12-slim

# Set the current working directory to usr/aa-Vector-DBs.
# This is where we'll put the requirements-dev.txt file and the app directory.
WORKDIR /usr/repos/vector-dbs

# Copy all application files to the container
COPY . /usr/repos/vector-dbs

# install system dependencies
RUN apt-get update \
  && apt-get -y install \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# install python dependencies
RUN pip3 install -U pip wheel setuptools \
    && pip3 install --no-cache-dir --upgrade -r requirements-dev.txt

# Keep the container running for interactive use
CMD ["tail", "-f", "/dev/null"]

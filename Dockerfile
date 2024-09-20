FROM python:3.10.12-slim
#FROM python:3.11

# Set the current working directory to usr/aa-Vector-DBs.
# This is where we'll put the requirements-dev.txt file and the app directory.
WORKDIR /usr/aa-Vector-DBs

# Copy requirements first and install them
COPY ./requirements-dev.txt /usr/aa-Vector-DBs/requirements-dev.txt

# Install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /usr/aa-Vector-DBs/requirements-dev.txt

# Copy all application files to the container
COPY . /usr/aa-Vector-DBs

# Keep the container running for interactive use
CMD ["tail", "-f", "/dev/null"]

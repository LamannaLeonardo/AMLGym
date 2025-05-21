# Define base image
FROM python:3.10-slim

# Set USER and USER_ID to run the docker container as a non root user
ARG USER=dkm
ARG USER_ID=1003
ARG USER_GROUP=standard
ARG USER_GROUP_ID=1003
ARG USER_HOME=/home/${USER}

# Create a user group and a user (this works only for debian based images)
RUN groupadd --gid $USER_GROUP_ID $USER \
    && useradd --uid $USER_ID --gid $USER_GROUP_ID -m $USER

# Setup image istructions
RUN apt-get update && apt-get install -y build-essential python3-dev curl swig g++ make

# Set container user
USER $USER

# Set the working directory in the container
WORKDIR /app

# Copy the project directory into the container
COPY requirements.txt /tmp/
COPY util/pddl-generators /app

# Compile pddl-generators
RUN cd /app/util/pddl-generators && ./build_all

# Install dependencies
RUN pip install -r /tmp/requirements.txt

# Run script as non-root user
ENTRYPOINT ["cd", "util", "&&", "python", "generators.py"]
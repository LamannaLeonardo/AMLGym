FROM ubuntu:22.04

# Install required packages
RUN apt-get update && apt-get -y install openjdk-8-jdk xvfb mesa-utils x11-xserver-utils xdotool gosu sudo acl curl zip unzip build-essential && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN apt-get update && apt-get -y install nano iputils-ping software-properties-common
RUN apt-get update && add-apt-repository -y ppa:deadsnakes/ppa -y

# Install python3.8
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Jerusalem
RUN apt-get update && apt install -y python3.8
RUN apt-get install -y python3.8-distutils
RUN curl https://bootstrap.pypa.io/get-pip.py | sudo python3.8

# Required for gym library
RUN pip install setuptools==66
RUN pip install wheel==0.38.4
RUN pip install protobuf==3.20.3

# Install numeric-sam
ADD METRIC_FF /METRIC_FF
ADD VAL /VAL
ADD numeric-sam /numeric-sam
RUN cd /numeric-sam && pip install -r requirements.txt
RUN cd /numeric-sam/tests && pytest
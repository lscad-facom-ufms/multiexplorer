FROM ubuntu:18.04

WORKDIR /multiexplorer/

RUN apt update

RUN apt install -y make
RUN apt install -y git
RUN apt install -y wget
RUN apt install -y python-minimal
RUN wget https://bootstrap.pypa.io/pip/2.7/get-pip.py
RUN python2 get-pip.py
RUN apt install -y python-tk

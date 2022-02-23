FROM ubuntu:18.04

WORKDIR /multiexplorer/

RUN apt update

RUN apt install -y python-minimal
RUN apt install -y wget
RUN wget https://bootstrap.pypa.io/pip/2.7/get-pip.py
RUN python2 get-pip.py
RUN apt install make
RUN apt install git

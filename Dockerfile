FROM ubuntu:18.04

WORKDIR /multiexplorer/

RUN apt update

RUN apt install -y make
RUN apt install -y git
RUN apt install -y wget

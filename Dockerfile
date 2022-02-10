FROM ubuntu:20.04

WORKDIR /multiexplorer/

RUN apt update
RUN apt install -y gcc-multilib
RUN apt install -y g++-multilib
RUN apt install -y python2
RUN python -m ensurepip --upgrade
RUN python -m pip install --upgrade pip

COPY . .

RUN pip2 install -r requirements.txt


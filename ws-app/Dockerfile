FROM ubuntu:22.04
RUN apt-get update && apt-get install -y python3 python3-pip

COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

EXPOSE 8001

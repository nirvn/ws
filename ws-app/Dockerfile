FROM ubuntu:24.04
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -qq -y python3 python3-pip && apt-get clean

COPY requirements.txt /requirements.txt
COPY app.py /app.py
RUN pip3 install -r /requirements.txt

CMD python3 /app.py

EXPOSE 8001

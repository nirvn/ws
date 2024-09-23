FROM ubuntu:24.04
RUN apt-get update && apt-get install -y python3 python3-pip

COPY requirements.txt /requirements.txt
COPY app.py /app.py
RUN pip3 install -r /requirements.txt

CMD python3 /app.py

EXPOSE 8001

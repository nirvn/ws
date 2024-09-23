FROM python:3.11

COPY requirements.txt /requirements.txt
COPY app.py /app.py
RUN pip3 install -r /requirements.txt

CMD ["python3", "/app.py"]

EXPOSE 8001

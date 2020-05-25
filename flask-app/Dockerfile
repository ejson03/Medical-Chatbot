FROM python:3.7-slim as base

WORKDIR /app/flask-app
ADD . /app/flask-app

RUN pip3 install -r  /app/flask-app/requirements.txt
VOLUME /app/flask-app

# CMD python3 app.py


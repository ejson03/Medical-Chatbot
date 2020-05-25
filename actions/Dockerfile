FROM rasa/rasa-sdk:latest
WORKDIR /app/actions
COPY requirements.txt /app/actions/requirements.txt
USER root
RUN apt-get update && apt-get -y install build-essential python3-dev libffi-dev \
    && python3 -m pip install --upgrade pip wheel \
    && pip3 install -r  /app/actions/requirements.txt \
    && python3 -m spacy download en_core_web_md
USER 1001
WORKDIR /app

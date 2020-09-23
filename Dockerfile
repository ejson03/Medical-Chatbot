FROM rasa/rasa:latest as base

FROM base as action
WORKDIR /app
COPY ./actions/requirements.txt /app/requirements.txt
USER root
RUN apt-get update && apt-get -y install build-essential python3-dev libffi-dev \
    && python3 -m pip install --upgrade pip wheel \
    && pip3 install -r  /app/requirements.txt \
    && python3 -m spacy download en_core_web_md
USER 1001
COPY ./actions /app/actions
ENTRYPOINT []
CMD ["python", "-m", "rasa_sdk", "--actions", "actions"]

FROM base as chatbot
WORKDIR /app
COPY ./chatbot /app
VOLUME /app
CMD [ "run","-m","/app/models", "--endpoint", "/app/endpoints.yml", "--credential", "/app/credentials.yml","--enable-api","--cors","*","--debug" ]

FROM rasa/rasa:1.10.1

WORKDIR /app
COPY . /app

VOLUME /app

CMD [ "run","-m","/app/models", "--endpoint", "/app/endpoints.yml", "--credential", "/app/credentials.yml","--enable-api","--cors","*","--debug" ]
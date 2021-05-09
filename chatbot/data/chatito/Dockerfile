FROM node:alpine

WORKDIR /app
RUN npm install -g chatito
ENTRYPOINT ["/bin/sh", "-c" , "npx chatito /app/data --format rasa --outputPath /app/results"]
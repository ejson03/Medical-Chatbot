FROM nginx:alpine
WORKDIR /app
ADD ./nginx.conf /etc/nginx/
COPY ./server.crt /app/server.crt
COPY ./server.key /app/server.key
EXPOSE 8443

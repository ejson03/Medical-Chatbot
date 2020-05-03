FROM ubuntu:18.04
ENV LANG C.UTF-8
RUN apt-get update && apt-get install -y python3 python3-pip curl python3-openssl
RUN python3 -m pip --no-cache-dir install --upgrade pip setuptools
ADD . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

RUN chmod +x /app/script.sh
CMD /app/script.sh

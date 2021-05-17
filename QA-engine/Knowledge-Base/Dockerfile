FROM python:slim

WORKDIR /app
RUN pip3 install python-dotenv py2neo pandas

COPY . .

CMD [ "python3", "build_medicalgraph.py"]
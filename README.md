# InterviewBot

ML and NLP based InterviewBot

To field questions relevant to an HR Interview and carry out a sustained conversation.
To process relevant user responses to evaluate and thus help the user better their interviewing skills.

## Setup

```
python3 -m venv venv
.\venv\Scripts\activate * for windows
source venv\bin\activate * for ubuntu
pip install -r requirements.txt
```

## Rasa Commands to execute 

For train
```
rasa train
```

For test
```
rasa test
```

For testing rest apis you have to run both action server and rasa main server
```
cd chatbot
rasa run actions
rasa run -m models --endpoint endpoints.yml --enable-api --cors “*” --debug --log-file out.log 
```

For running main web app
```
cd flask-app
python app.py
```

## For connecting to rasa APi
Create a tracker store in mongodb, checkout endpoints.yml
For interacting with bot on WEbUi query message, userid to http://<rasa-server-ip-address>:5005/webhooks/rest/webhook

## Errors in the above platform
Check the stories and alter rasa.js based on them
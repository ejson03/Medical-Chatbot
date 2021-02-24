CALL rasa/Scripts/activate.bat
CALL cd actions && rasa run actions
CALL cd chatbot && rasa run -m models --endpoint endpoints.yml --credentials credentials.yml --enable-api --debug --cors “*”
CALL npm start
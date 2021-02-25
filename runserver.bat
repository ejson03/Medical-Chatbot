@CALL rasa/Scripts/activate.bat
@start /b cmd /c "cd actions && rasa run actions"
@start /b cmd /c "cd chatbot && rasa run -m models --endpoint endpoints.yml --credentials credentials.yml --enable-api --debug"
@start /b cmd /c "npm start"

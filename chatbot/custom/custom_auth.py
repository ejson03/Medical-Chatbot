import logging
import uuid
import json
from sanic import Blueprint, response
from rasa.core.channels.channel import InputChannel
from sanic.request import Request
from datetime import datetime, timedelta
import jwt
from os import environ

SECRET_KEY = environ.get("JWT_SECRET")
logger = logging.getLogger(__name__)

class Token(InputChannel):

    @classmethod
    def name(cls):
        return "token"

    def blueprint(self, on_new_message):
        token_webhook = Blueprint(
            'token_webhook', __name__
        )

        @token_webhook.route("/", methods=["GET"])
        async def health(request: Request):
            return response.json({"status": "ok"})

        @token_webhook.route("/webhook", methods=["POST"])
        async def receive(request):
            if not request.json:
                return response.json({"error":"Missing sender"}, 400)

            sender_id = request.json.get("sender", None)
            role = request.json.get("role", None)
            print("Sender ID: ", sender_id)
            utcnow = datetime.utcnow() + timedelta(seconds=-5)
            expires = utcnow + timedelta(hours=24)                     
            try:
                payload = {'iat': utcnow,'user_id': sender_id, 'role': role, 'exp':expires}
                bot_token = jwt.encode( payload,
                                    SECRET_KEY, 
                                    algorithm='HS256')
            except Exception as e:
                return response.json({'error':str(e)}, 400)
            return response.json({"bot_token": bot_token}, 200)
            
            
        return token_webhook



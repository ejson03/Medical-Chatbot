import logging
import uuid
import inspect
import rasa
from sanic import Blueprint, response, Sanic
from sanic.request import Request
from socketio import AsyncServer
from asyncio import Queue, CancelledError
from rasa.core.channels.channel import UserMessage, OutputChannel, CollectingOutputChannel, InputChannel
import jwt
from os import environ
from io import BytesIO
import base64


logger = logging.getLogger(__name__)
SECRET_KEY = environ.get("SECRET_KEY")

def jwt_decode(token):
    try:
        query = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return query
    except:
        return False

class RestInput(InputChannel):
    """A custom http input channel

    This implementation is the basis for a custom implementation of a chat
    frontend. You can customize this to send messages to Rasa Core and
    retrieve responses from the agent."""

    @classmethod
    def name(cls):
        return "rest"

    @staticmethod
    async def on_message_wrapper(on_new_message, text, queue, sender_id) :

        collector = QueueOutputChannel(queue)

        message = UserMessage(
            text, collector, sender_id, input_channel= RestInput.name()
        )

        await on_new_message(message)

        await queue.put("DONE")  # pytype: disable=bad-return-type

    async def _extract_sender(self, req) :
        return req.get("user_id", None)

    async def _extract_message(self, req):
        return req.json.get("message", None)

    async def _extract_file(self, req):
        return base64.b64encode(req.files['file'][0][1]).decode('ascii')

    async def _extract_header(self, req) :
        return req.headers.get("Authorization", None)

    def stream_response(self, on_new_message, text, sender_id ) :
        async def stream(resp):
            q = Queue()
            task = asyncio.ensure_future(
                self.on_message_wrapper(on_new_message, text, q, sender_id)
            )
            while True:
                result = await q.get() 
                if result == "DONE":
                    break
                else:
                    await resp.write(json.dumps(result) + "\n")
            await task

        return stream  

    def blueprint(self, on_new_message):
        custom_webhook = Blueprint(
            "custom_webhook_{}".format(type(self).__name__),
            inspect.getmodule(self).__name__,
        )

        @custom_webhook.route("/", methods=["GET"])
        async def health(request: Request):
            return response.json({"status": "ok"})

        @custom_webhook.route("/webhook", methods=["POST"])
        async def receive(request: Request):
            jwt_data = await self._extract_header(request)
            jwt_data = jwt_decode(jwt_data)
            try:
                text = await self._extract_message(request)
                should_use_stream = rasa.utils.endpoints.bool_arg(
                    request, "stream", default=False
                )
            except:
                text = await self._extract_file(request)
                should_use_stream = rasa.utils.endpoints.bool_arg(
                    request, "stream", default=False
                )

            if(jwt_data):
                sender_id = await self._extract_sender(jwt_data)
                if should_use_stream:
                    return response.stream(
                        self.stream_response(on_new_message, text, sender_id),
                        content_type="text/event-stream",
                        
                    )
                else:
                    collector = CollectingOutputChannel()
                    try:
                        await on_new_message(
                            UserMessage(
                                text, collector, sender_id, input_channel=self.name()
                            )
                        )
                    except CancelledError:
                        logger.error(
                            "Message handling timed out for "
                            "user message '{}'.".format(text)
                        )
                    except Exception:
                        logger.exception(
                            "An exception occured while handling "
                            "user message '{}'.".format(text)
                        )
                    return response.json(collector.messages)
            else: 
                return response.json({"Error": "error"})
                
        return custom_webhook



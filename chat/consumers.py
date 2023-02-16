import json
import logging
from asgiref.sync import async_to_sync

from channels.generic.websocket import WebsocketConsumer

logger = logging.getLogger(__name__)


class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        logger.info('ChatConsumer init')
        super().__init__(args, kwargs)
        self.room_group_name = None
        self.room_name = None

    def connect(self):
        logger.info('connect ChatConsumer')
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        # he wrapper is required because ChatConsumer is
        # a synchronous WebsocketConsumer
        # but it is calling an asynchronous channel layer method.
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        # Accepts the WebSocket connection.
        # If you do not call within the method then the connection will be rejected and closed.
        #
        self.accept()

    def disconnect(self, code):
        logger.info('disconnect ChatConsumer')
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        logger.info('receive message is %s', message)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    # handler for message type chat_message
    # room_group_name 中有多少 channel_name 该方法 在 每个 ChatConsumer 都有一个
    def chat_message(self, event):
        logger.info('chat_message event is %s', event)
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))

from django.urls import re_path

from chat import consumers

websocket_urlpatterns = [
    # re_path = partial(_path, Pattern=RegexPattern) re 正则的意思
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]

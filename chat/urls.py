from django.urls import re_path

from chat import views  #等同于views.py 稍后创建

urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', views.ChatConsumer.as_asgi()),
]

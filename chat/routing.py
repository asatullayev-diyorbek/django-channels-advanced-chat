from django.urls import re_path
from .consumers import ChatConsumer, ProfileListConsumer


websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<name>\w+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/users/$', ProfileListConsumer.as_asgi()),
]
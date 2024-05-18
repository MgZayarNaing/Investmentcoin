from django.urls import path,re_path

from . import consumers
from .consumers import CountdownConsumer


websocket_urlpatterns = [
    path('ws/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
    path('ws/countdown/', CountdownConsumer.as_asgi()),
]
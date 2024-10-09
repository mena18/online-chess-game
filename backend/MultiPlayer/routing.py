# chat/routing.py
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(
        "ws/MultiPlayerGame/<room_name>/", consumers.MultiPlayerGameConsumer.as_asgi()
    ),
]

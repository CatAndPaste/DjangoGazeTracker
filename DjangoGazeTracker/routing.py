from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/video/', consumers.CameraConsumer.as_asgi()),
]

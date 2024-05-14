# import os

# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.security.websocket import AllowedHostsOriginValidator
# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Coin.settings')

# from chat import routing

# django_asgi_application = get_asgi_application()

# application = ProtocolTypeRouter(
#     {
#         'http': django_asgi_application,
#         'websocket': AllowedHostsOriginValidator(
#             AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns))
#         )
#     }
# )

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from chat.consumers import ChatConsumer, CountdownConsumer

websocket_urlpatterns = [
    # path('ws/chat/<str:room_name>/', ChatConsumer.as_asgi()),
    path('ws/countdown/', CountdownConsumer.as_asgi()),
    path('ws/<str:room_name>/', ChatConsumer.as_asgi()),
    
]

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})

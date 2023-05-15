import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django_asgi_app  = get_asgi_application()

import myproject.stats.routing

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        #"websocket": URLRouter([path("real-time/", RealTimeConsumer.as_asgi())]),
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(myproject.stats.routing.websocket_urlpatterns))
        )

        # Just HTTP for now. (We can add other protocols later.)
    }
)
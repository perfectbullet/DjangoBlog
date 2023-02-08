"""
ASGI config for TestVideos project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoBlog.settings')

# application = get_asgi_application()  #原本内容


from channels.routing import ProtocolTypeRouter, URLRouter  #channels
from channels.auth import AuthMiddlewareStack
from chat import urls  #我们创建的app


application = ProtocolTypeRouter({
    # "http": get_asgi_application(), #此处会影响http请求。此处大概时异步接管HTTP的意思

    "websocket": AuthMiddlewareStack(
        URLRouter(
            urls.urlpatterns
        )
    ),
})

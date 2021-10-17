from channels import AuthMiddleWareStack
from channels.routing import ProtocolTypeRouter, URLRouter

application = ProtocolTypeRouter({
    'websocket': AuthMiddleWareStack(
        
    )
})

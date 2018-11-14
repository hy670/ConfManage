from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter, ProtocolTypeRouter
from django.conf.urls import url
from ConfManage.djchannels import wssh

application = ProtocolTypeRouter({
	"websocket": AuthMiddlewareStack(
		URLRouter([
			url(r'^ws/webssh/(?P<id>[0-9]+)/$$',wssh.Webterminal),

			# path(r"stats/", StatsConsumer),
		])
	)
})

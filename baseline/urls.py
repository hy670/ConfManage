from django.conf.urls import url
from .views import check_rule

urlpatterns = [
	url(r'^RegexGroupLis/$', check_rule.check_rule),
	url(r'^RegexGroupDetail/(?P<group_id>[0-9]+)$', check_rule.regex_group_detail),


]

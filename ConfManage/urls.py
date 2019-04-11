"""ConfManage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from ConfManage.views import index, policy, users, assets, wssh, conf_file, topo, conf_bak

urlpatterns = [
	url(r'^$', index.index),
	url(r'^admin/', admin.site.urls),
	url(r'^index/', index.index),
	url(r'^login/', index.login),
	url(r'^logout', index.logout),
	url(r'^config', index.config),
	url(r'^noperm', index.noperm),
	url(r'^assets_line', assets.assets_line),
	url(r'^assets_add', assets.assets_add),
	url(r'^assets_list/', assets.assets_list),
	url(r'^assets_mod/(?P<aid>[0-9]+)/$', assets.assets_modf),
	url(r'^assets_view/(?P<aid>[0-9]+)/$', assets.assets_view),
	url(r'^assets_facts', assets.assets_facts),
	url(r'^assets_log/(?P<page>[0-9]+)/$', assets.assets_log),
	url(r'^assets_import/', assets.assets_import),
	url(r'^assets_search/', assets.assets_search),
	url(r'^assets_server/', assets.assets_server),
	url(r'^assets/batch/update/', assets.assets_update),
	url(r'^assets/batch/delete/', assets.assets_delete),
	url(r'^assets/batch/dumps/', assets.assets_dumps),
	url(r'^assets/groups/(?P<id>[0-9]+)/$', assets.assets_groups),
	url(r'^policy_zone/', policy.policy_zone),
	url(r'^policy_list/', policy.policy_list),
	url(r'^policy_search/', policy.policy_search),
	url(r'^policy_redundancy_check/', policy.policy_redundancy_check),
	url(r'^policy_iszmbie_check/', policy.policy_iszmbie_check),
	url(r'^policy_regular_list/', policy.policy_regular_list),
	url(r'^policy_regular_check/', policy.policy_regular_check),
	url(r'^user/center/$', users.user_center),
	url(r'^user/server/(?P<uid>[0-9]+)/$', users.user_server),
	url(r'^users/manage$', users.user_manage),
	url(r'^webssh/list/$', wssh.wssh_list),
	url(r'^webssh/(?P<sid>[0-9]+)/$', wssh.wssh),
	url(r'^conffile/list/$', conf_file.conffile_list),
	url(r'^conffile/diff/$', conf_file.conffile_diff),
	url(r'^topo_graph/$', topo.topo_graph),
	url(r'^topo_edge/$', topo.topo_edge),

]

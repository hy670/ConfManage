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
from ConfManage.views import (index, policy)

urlpatterns = [
	url(r'^$', index.index),
	url(r'^admin/', admin.site.urls),
	url(r'^index/', index.index),
	url(r'^login/', index.login),
	url(r'^logout', index.logout),
	url(r'^config', index.config),
	url(r'^noperm', index.noperm),
	url(r'^policy_list/', policy.policy_list),
	url(r'^policy_search/', policy.policy_search),
	url(r'^policy_redundancy_check/', policy.policy_redundancy_check),
	url(r'^policy_iszmbie_check/', policy.policy_iszmbie_check),
	url(r'^policy_regular_list/', policy.policy_regular_list),
	url(r'^policy_regular_check/', policy.policy_regular_check),

]

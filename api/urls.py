from django.conf.urls import url
from .views import (wiki_api,assets_api,deploy_api,cron_api,
                       logs_api,ansible_api,db_api,users_api,
                       orders_api,files_api,task_api)
urlpatterns = [

            url(r'^group/$', assets_api.group_list), 
            url(r'^group/(?P<id>[0-9]+)/$',assets_api.group_detail), 
            url(r'^user/$', users_api.user_list), 
            url(r'^user/(?P<id>[0-9]+)/$',users_api.user_detail), 

    ]    
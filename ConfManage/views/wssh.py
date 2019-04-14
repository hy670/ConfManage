#!/usr/bin/env python
# _#_ coding:utf-8 _*_
from django.db.models import Count
from django.shortcuts import render
from ConfManage.models import Assets, Network_Assets
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from ConfManage.utils.logger import logger

@login_required(login_url='/login')
@permission_required('ConfManage.views_webssh', login_url='/noperm/')
def wssh_list(request):
	assetsList = Assets.objects.all().order_by("-id")

	assetsNumber = Assets.objects.values('assets_type').annotate(dcount=Count('assets_type'))
	return render(request, 'webssh/ssh_list.html', {"user": request.user, "totalAssets": assetsList.count(),
	                                                   "assetsList": assetsList, "assetsNumber": assetsNumber
	                                                    })

@login_required(login_url='/login')
@permission_required('ConfManage.views_webssh', login_url='/noperm/')
def wssh(request, sid):
	try:
		server = Network_Assets.objects.get(assets_id=sid)
		if request.user.is_superuser:
			serverList = Network_Assets.objects.all()
			return render(request, 'webssh/webssh.html', {"user": request.user, "server": server,
														  "serverList": serverList})
		else:
			user_server = Network_Assets.objects.get(user_id=request.user.id, server_id=sid)
			userServer = Network_Assets.objects.filter(user_id=request.user.id)
			serverList = []
			for s in userServer:
				ser = Network_Assets.objects.get(id=s.server_id)
				serverList.append(ser)
			if user_server:
				return render(request, 'webssh/webssh.html', {"user": request.user, "server": server,
															  "serverList": serverList})
	except Exception as ex:
		logger.error(msg="请求webssh失败: {ex}".format(ex=str(ex)))
		return render(request, 'webssh/webssh.html', {"user": request.user, "errorInfo": "你没有权限访问这台服务器！"})

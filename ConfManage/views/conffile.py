#!/usr/bin/env python
# _#_ coding:utf-8 _*_
import os

from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from ConfManage.models import Assets, Network_Assets,Conffile
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from ConfManage.utils.logger import logger

@login_required(login_url='/login')
def conffile_list(request):
	if request.method == 'GET':
		assets = Network_Assets.objects.filter(is_master=True)
		conffiledic = []
		for conffile in Conffile.objects.all():
			devname =Network_Assets.objects.get(id=conffile.network_assets_id).hostname
			conffiledic.append({'id':conffile.id,'hostname':devname,'filename':conffile.filename,'date':conffile.create_date,
								'file_detail':conffile.file_detail})
		return render(request, 'filemanage/file_download_list.html',{'assets':assets,'conffile':conffiledic})
	elif request.method == 'POST':
		print(os.getcwd())
		assets_id =request.POST.get('assets_name')
		file_detail = request.POST.get('conffile_detail')
		f = request.FILES.get('import_file')
		assets = Network_Assets.objects.get(id=assets_id)
		Conffile.objects.create(filename=f.name,file_detail=file_detail,network_assets=assets)
		filename = os.path.join(os.getcwd() + '/conffile/', f.name)
		if os.path.isdir(os.path.dirname(filename)) is not True: os.makedirs(os.path.dirname(filename))
		fobj = open(filename, 'wb')
		for chrunk in f.chunks():
			fobj.write(chrunk)
		fobj.close()
		return JsonResponse({'msg': "修改成功~", "code": '502'})




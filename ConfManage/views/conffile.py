#!/usr/bin/env python
# _#_ coding:utf-8 _*_
import os

from django.db.models import Count
from django.shortcuts import render
from ConfManage.models import Assets, Network_Assets
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from ConfManage.utils.logger import logger

@login_required(login_url='/login')
def conffile_list(request):
	if request.method == 'GET':
		assets = Network_Assets.objects.filter(is_master=True)
		return render(request, 'filemanage/file_download_list.html',{'assets':assets})
	elif request.method == 'POST':
		print(os.getcwd())
		f = request.FILES.get('import_file')
		filename = os.path.join(os.getcwd() + '/conffile/', f.name)
		if os.path.isdir(os.path.dirname(filename)) is not True: os.makedirs(os.path.dirname(filename))
		fobj = open(filename, 'wb')
		for chrunk in f.chunks():
			fobj.write(chrunk)
		fobj.close()




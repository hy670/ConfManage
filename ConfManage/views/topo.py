#!/usr/bin/env python
# _#_ coding:utf-8 _*_
from datetime import *
import os
import difflib

import chardet
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from ConfManage.models import Assets, Network_Assets,Conffile,Line_Assets
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from ConfManage.utils.logger import logger


@login_required(login_url='/login')
def topo_graph(request):
	if request.method == 'GET':
		nodelist =[]
		for asset in Assets.objects.all():
			if asset.assets_type in ['switch','route','firewall']:
				net_asset = Network_Assets.objects.get(assets_id=asset.id)
				nodelist.append({'name':net_asset.hostname,'type':asset.assets_type})
		return render(request, 'topo/topo_graph.html',{'nodelist':nodelist})
	elif request.method == 'POST':
		if request.POST.get('op')=='add':
			print(os.getcwd())
			assets_id =request.POST.get('assets_name')
			file_detail = request.POST.get('conffile_detail')
			assets = Network_Assets.objects.get(id=assets_id)
			f = request.FILES.get('import_file')
			filename = assets.hostname+'-'+datetime.now().strftime("%Y%m%d%H%M%S")+"."+f.name.split(".")[-1]
			filepath = os.path.join(os.getcwd() + '/conffile/', filename)
			if os.path.isdir(os.path.dirname(filepath)) is not True: os.makedirs(os.path.dirname(filepath))
			fobj = open(filepath, 'wb')
			for chrunk in f.chunks():
				fobj.write(chrunk)
			fobj.close()
			Conffile.objects.create(filename=filename, file_detail=file_detail, network_assets=assets)
			return JsonResponse({'msg': "修改成功~", "code": '502'})
		elif request.POST.get('op') == 'del':
			id =request.POST.get('file_id')
			f = Conffile.objects.get(id=id)
			filename = os.path.join(os.getcwd() + '/conffile/', f.filename)
			if os.path.exists(filename):
				os.remove(filename)
				f.delete()
				return JsonResponse({'msg': "文件已删除~", "code": '502'})
			else:
				f.delete()
				return JsonResponse({'msg': "文件已删除~", "code": '502'})

@login_required(login_url='/login')
def conffile_diff(request):
	if request.method == 'GET':
		assets = Network_Assets.objects.filter(is_master=True)
		conffiledic = []
		for conffile in Conffile.objects.all().order_by('-create_date'):
			devname =Network_Assets.objects.get(id=conffile.network_assets_id).hostname
			conffiledic.append({'id':conffile.id,'hostname':devname,'filename':conffile.filename,'date':conffile.create_date,
								'file_detail':conffile.file_detail})
		return render(request, 'filemanage/file_diff.html',{'assets':assets,'conffile':conffiledic})
	elif request.method == 'POST':
		if request.POST.get('op')=='list_conffile':
			assets_id =request.POST.get('file_id')
			files_query = Conffile.objects.filter(network_assets=assets_id)
			files = []
			for file in files_query:
				files.append({"conffile.id":file.id,"conffile.name":file.filename})
			return JsonResponse({'msg': "修改成功~", "files":files})
		elif request.POST.get('op')=='compare_conffile':
			file1 = request.POST.get('file1')
			file2 = request.POST.get('file2')
			filename1 = os.path.join(os.getcwd() + '/conffile/', Conffile.objects.get(id=file1).filename)
			filename2 = os.path.join(os.getcwd() + '/conffile/', Conffile.objects.get(id=file2).filename)
			with open(filename1, "rb") as f:
				data = f.read()
				encode = chardet.detect(data)
			try:
				f1 = open(filename1, 'r', encoding=encode["encoding"])
				f2 = open(filename2, 'r', encoding=encode["encoding"])
			except IOError:
				print("ERROR: 没有找到文件:或读取文件失败！")
			d = difflib.HtmlDiff()
			result = d.make_file(f1.readlines(), f2.readlines())
			return JsonResponse({'msg': "修改成功~", "result": result})





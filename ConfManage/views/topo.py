#!/usr/bin/env python
# _#_ coding:utf-8 _*_
from datetime import *
import os
from importlib import reload
from django.http import JsonResponse
from django.shortcuts import render
from ConfManage.models import Assets, Network_Assets,Server_Assets,Line_Assets,Edges,Server_Edges,Network_Edges,Line_Edges
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
import ConfManage.utils.topograph
from ConfManage.utils.topograph import Topo
from ConfManage.utils.logger import logger


@login_required(login_url='/login')
def topo_graph(request):
	if request.method == 'GET':
		reload(ConfManage.utils.topograph)
		from ConfManage.utils.topograph import Topo
		nodelist = Topo.nodes
		edgelist =Topo.edges
		topo = {'nodes':nodelist,'edges':edgelist}
		return render(request, 'topo/topo_graph.html',{'topo':topo})
	elif request.method == 'POST':
		pass

@login_required(login_url='/login')
def topo_edge(request):
	if request.method == 'GET':
		return render(request, 'topo/topo_edge.html')
	elif request.method == 'POST':
		if request.POST.get('op')=='type_select':
			srcdic = []
			dstdic = []
			link_type = request.POST.get('link_type')
			netasset = Network_Assets.objects.filter(is_master=True)
			for net in netasset:
				srcdic.append({'id':net.id,'name':net.hostname})
			if link_type == "server":
				serverasset = Server_Assets.objects.all()
				for server in serverasset:
					dstdic.append({'id': server.id, 'name': server.hostname})
				return JsonResponse({'src':srcdic,'dst':dstdic})
			elif link_type == "net":
				return JsonResponse({'src': srcdic, 'dst': srcdic})
			elif link_type == "line":
				lineasset = Line_Assets.objects.filter(line_is_master=True)
				for line in lineasset:
					dstdic.append({'id': line.id, 'name': line.line_name})
				return JsonResponse({'src': srcdic, 'dst': dstdic})
		elif request.POST.get('op')=='add_link':
			link_type = request.POST.get('link_type')
			src = request.POST.get('src')
			dst = request.POST.get('dst')
			print(link_type)
			print(src)
			print(dst)
			try:
				srcasset = Network_Assets.objects.get(id=src)
			except Exception as ex:
				print(ex)
			try:
				edge = Edges.objects.create(edges_type=link_type)
			except Exception as ex:
				print(ex)
			if link_type == "server":
				dstasset =Server_Assets.objects.get(id=dst)
				try:
					Server_Edges.objects.create(Edges=edge,src=srcasset,dst=dstasset)
				except Exception as ex:
					print(ex)
					edge.delete()
				return JsonResponse({'msg':'添加成功'})
			elif link_type == "net":
				dstasset = Network_Assets.objects.get(id=dst)
				try:
					Network_Edges.objects.create(Edges=edge, src=srcasset, dst=dstasset)
				except Exception as ex:
					print(ex)
					edge.delete()
				return JsonResponse({'msg': '添加成功'})
			elif link_type == "line":
				dstasset = Line_Assets.objects.get(id=dst)
				try:
					Line_Edges.objects.create(Edges=edge, src=srcasset, dst=dstasset)
				except Exception as ex:
					print(ex)
					edge.delete()
				return JsonResponse({'msg': '添加成功'})






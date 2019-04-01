#!/usr/bin/env python
# _#_ coding:utf-8 _*_
from datetime import *
import os
from importlib import reload
from django.http import JsonResponse
from django.shortcuts import render
from ConfManage.models import *
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
import ConfManage.utils.topograph
from ConfManage.utils.topograph import Topo
from ConfManage.utils.logger import logger
from django.db import transaction


@login_required(login_url='/login')
def topo_graph(request):
	if request.method == 'GET':
		reload(ConfManage.utils.topograph)
		from ConfManage.utils.topograph import Topo
		nodelist = Topo.nodes
		edgelist = Topo.edges
		topo = {'nodes': nodelist, 'edges': edgelist}
		return render(request, 'topo/topo_graph.html', {'topo': topo})
	elif request.method == 'POST':
		pass


@login_required(login_url='/login')
def topo_edge(request):
	if request.method == 'GET':
		edges = Edges.objects.all()
		seredges = Server_Edges.objects.all()
		netedges = Network_Edges.objects.all()
		lineedges = Line_Edges.objects.all()

		edgesdic = []
		for edge in edges:
			edgeid = edge.id
			edgetype = edge.edges_type
			if edgetype == "net":
				for netedge in netedges:
					if edge.id == netedge.Edges_id:
						srcdev = Network_Assets.objects.get(id=netedge.src_id).hostname
						dstdev = Network_Assets.objects.get(id=netedge.dst_id).hostname
			elif edge.edges_type == "line":
				for lineedge in lineedges:
					if edge.id == lineedge.Edges_id:
						srcdev = Network_Assets.objects.get(id=lineedge.src_id).hostname
						dstdev = Line_Assets.objects.get(id=lineedge.dst_id).line_name
			elif edge.edges_type == "server":
				for seredge in seredges:
					if edge.id == seredge.Edges_id:
						srcdev = Network_Assets.objects.get(id=seredge.src_id).hostname
						dstdev = Server_Assets.objects.get(id=seredge.dst_id).hostname
			edgesdic.append({'id': str(edgeid), 'type': edgetype, 'srcdev': srcdev, 'dstdev': dstdev})
		return render(request, 'topo/topo_edge.html', {'edges': edgesdic})
	elif request.method == 'POST':
		if request.POST.get('op') == 'type_select':
			srcdic = []
			dstdic = []
			link_type = request.POST.get('link_type')
			netasset = Network_Assets.objects.filter(is_master=True)
			for net in netasset:
				srcdic.append({'id': net.id, 'name': net.hostname})
			if link_type == "server":
				serverasset = Server_Assets.objects.all()
				for server in serverasset:
					dstdic.append({'id': server.id, 'name': server.hostname})
				return JsonResponse({'src': srcdic, 'dst': dstdic})
			elif link_type == "net":
				return JsonResponse({'src': srcdic, 'dst': srcdic})
			elif link_type == "line":
				lineasset = Line_Assets.objects.filter(line_is_master=True)
				for line in lineasset:
					dstdic.append({'id': line.id, 'name': line.line_name})
				return JsonResponse({'src': srcdic, 'dst': dstdic})
		elif request.POST.get('op') == 'add_link':
			link_type = request.POST.get('link_type')
			src = request.POST.get('src')
			dst = request.POST.get('dst')
			try:
				srcasset = Network_Assets.objects.get(id=src)
			except Exception as e:
				logger.warn("查询资产错误，错误原因：%s", e)
			try:
				edge = Edges.objects.create(edges_type=link_type)
			except Exception as ex:
				logger.warn("增加edge错误，错误原因：%s", e)
			if link_type == "server":
				dstasset = Server_Assets.objects.get(id=dst)
				try:
					Server_Edges.objects.create(Edges=edge, src=srcasset, dst=dstasset)
				except Exception as e:
					logger.warn("增加edge错误，错误原因：%s", e)
					edge.delete()
				return JsonResponse({'msg': '添加成功'})
			elif link_type == "net":
				dstasset = Network_Assets.objects.get(id=dst)
				try:
					Network_Edges.objects.create(Edges=edge, src=srcasset, dst=dstasset)
				except Exception as ex:
					logger.warn("增加edge错误，错误原因：%s", e)
					edge.delete()
				return JsonResponse({'msg': '添加成功'})
			elif link_type == "line":
				dstasset = Line_Assets.objects.get(id=dst)
				try:
					Line_Edges.objects.create(Edges=edge, src=srcasset, dst=dstasset)
				except Exception as ex:
					logger.warn("增加edge错误，错误原因：%s", e)
					edge.delete()
				return JsonResponse({'msg': '添加成功'})
		elif request.POST.get('op') == 'del_edge':
			id = request.POST.get('id')
			edge = Edges.objects.get(id=id)
			if edge.edges_type == "net":
				try:
					with transaction.atomic():
						Network_Edges.objects.get(Edges_id=id).delete()
						edge.delete()
				except Exception as e:
					logger.debug("删除Edge错误，错误原因：%s", e)
					return JsonResponse({'msg': "删除失败~", "code": '500'})
				return JsonResponse({'msg': "删除成功~", "code": '400'})
			elif edge.edges_type == "line":
				try:
					with transaction.atomic():
						Line_Edges.objects.get(Edges_id=id).delete()
						edge.delete()
				except Exception as e:
					logger.debug("删除Edge错误，错误原因：%s", e)
					return JsonResponse({'msg': "删除失败~", "code": '500'})
				return JsonResponse({'msg': "删除成功~", "code": '400'})
			elif edge.edges_type == "server":
				try:
					with transaction.atomic():
						Server_Edges.objects.get(Edges_id=id).delete()
						edge.delete()
				except Exception as e:
					logger.debug("删除Edge错误，错误原因：%s", e)
					return JsonResponse({'msg': "删除失败~", "code": '500'})
				return JsonResponse({'msg': "删除成功~", "code": '400'})

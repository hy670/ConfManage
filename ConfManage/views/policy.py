#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
from importlib import reload

import json
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ConfManage.utils.is_ip import is_ip
from ConfManage.utils.logger import logger
from ConfManage.utils.topograph import Topo, searchpolicy, regularcheck,iszmbiepolicy
from ConfManage.models import Applied_policy, Network_Assets, Assets, Server_Assets, Line_Assets, Firewall_Policy_Zone


@login_required(login_url='/login')
@permission_required('ConfManage.views_policy', login_url='/noperm/')
def policy_list(request):
	if request.method == "GET":
		firewalllist = []
		for nxnode in Topo.nxtopology.nodes:
			if nxnode.type == "firewall":
				firewalllist.append({'name': nxnode.name})
		return render(request, 'policy/policy_list.html', {'firewalllist': firewalllist})
	elif request.method == "POST":
		policydiclist = []
		dev = request.POST.get('dev')
		for nxnode in Topo.nxtopology.nodes:
			if dev == nxnode.name:
				for i in nxnode.policymiclist:
					temppolicydic = {'dev': nxnode.name, 'id': i.policyid, 'srceth': i.srceth, 'dsteth': i.dsteth,
					                 'srcaddr': i.srcaddr, 'dstaddr': i.dstaddr, 'protocol': i.service['protocol'],
					                 'port': i.service['port']}
					policydiclist.append(temppolicydic)
				return JsonResponse({'msg': '200', 'policy': policydiclist})


@login_required(login_url='/login')
@permission_required('ConfManage.views_policy', login_url='/noperm/')
def policy_zone(request):
	if request.method == "GET":
		firewalllist = []
		nodeslist = []
		zonelist = []
		for nxnode in Topo.nxtopology.nodes:
			if nxnode.type == "firewall":
				firewalllist.append({'assetid':nxnode.assetid, 'name': nxnode.name})
			nodeslist.append({'assetid':nxnode.assetid,'name': nxnode.name})
		zones = Firewall_Policy_Zone.objects.all()
		for zone in zones:
			zonelist.append({'id':zone.id, 'firewall':zone.Network_Assets.hostname,'zone':zone.zone, 'asset_type':zone.assets_type, 'asset_name':zone.assets_name})
		return render(request, 'policy/policy_zone.html', {'nodes': nodeslist, 'firewalllist': firewalllist,'zonelist':zonelist})
	elif request.method == "POST":
		if request.POST.get('op') == 'add_policy_zone':
			firewall = request.POST.get('firewall')
			zone = request.POST.get('zone')
			dstdev_group = json.loads(request.POST.get('dstdev_group'))
			for dstdev in dstdev_group:
				for nxnode in Topo.nxtopology.nodes:
					if nxnode.name == dstdev:
						netasset = Network_Assets.objects.get(id=int(firewall))
						Firewall_Policy_Zone.objects.create(Network_Assets=netasset,zone=zone,assets_type=nxnode.type,assets_name=nxnode.name)
			return JsonResponse({'msg':"安全域配置成功", "code": '400'})
		elif request.POST.get('op') == 'dev_select':
			assetid = request.POST.get('assetid')
			nodeslist = []
			for nxnode in Topo.nxtopology.nodes:
				if  nxnode.type == "firewall" and nxnode.assetid == int(assetid):
					zonelist =nxnode.zone
				else:
					nodeslist.append({'assetid': nxnode.assetid, 'name': nxnode.name})
			return JsonResponse({'zone':zonelist ,'nodes':nodeslist, "code": '400'})
		elif request.POST.get('op') == 'del_zone':
			id = request.POST.get('id')
			Firewall_Policy_Zone.objects.get(id=id).delete()
			return JsonResponse({'msg': "安全域删除成功", "code": '400'})



@login_required(login_url='/login')
@permission_required('ConfManage.views_policy', login_url='/noperm/')
def policy_search(request):
	if request.method == "GET":
		return render(request, 'policy/policy_search.html')
	elif request.method == "POST":
		dev = request.POST.get('dev')
		srcaddr = request.POST.get('srcaddr')
		dstaddr = request.POST.get('dstaddr')
		protocol = request.POST.get('protocol')
		port = request.POST.get('port')
		nodes = []
		edges = []
		if not protocol:
			protocol = '0'
		if not port:
			port = 0
		if not is_ip(srcaddr) and not is_ip(dstaddr):
			return JsonResponse({'msg': "请输入合法IP地址~", "code": '502'})
		elif int(port) not in range(0, 65535):
			return JsonResponse({'msg': "请输入正确端口号，范围1-66535~", "code": '502'})
		else:
			print(srcaddr)
			print(dstaddr)
			print(protocol)
			print(port)
			policydiclist = []
			routelist,tempdic = searchpolicy(srcaddr, dstaddr, protocol, port)
			if routelist == False and tempdic == False:
				return JsonResponse({'msg': "输入的地址不在拓扑内，如存在请添加节点！！", "code": '502'})
			for i in range(0,len(routelist)):
				nodes.append({'id': routelist[i].name, 'label': routelist[i].name, 'type': routelist[i].type})
				if i < len(routelist)-1:
					edges.append({"from":routelist[i].name,"to":routelist[i+1].name})
			for key in tempdic:
				if len(tempdic[key]) > 0:
					for i in tempdic[key]:
						temppolicydic = {'dev': key,
						                 'id': i.policyid,
						                 'srceth': i.srceth,
						                 'dsteth': i.dsteth,
						                 'srcaddr': i.srcaddr,
						                 'dstaddr': i.dstaddr,
						                 'protocol': i.service['protocol'],
						                 'port': i.service['port']}
						policydiclist.append(temppolicydic)
			return JsonResponse({'policy': policydiclist,'nodes':nodes,'edges':edges, "code": '400'})


@login_required(login_url='/login')
@permission_required('ConfManage.views_policy', login_url='/noperm/')
def policy_redundancy_check(request):
	if request.method == "GET":
		firewalllist = []
		for nxnode in Topo.nxtopology.nodes:
			if nxnode.type == "firewall":
				firewalllist.append({'name': nxnode.name})
		return render(request, 'policy/policy_redundancy_check.html', {'firewalllist': firewalllist})
	elif request.method == "POST":
		policydiclist = []
		dev = request.POST.get('dev')
		for nxnode in Topo.nxtopology.nodes:
			if dev == nxnode.name:
				policydiclist = nxnode.redundantcheck()
				return JsonResponse({'msg': '200', 'policy': policydiclist})


@login_required(login_url='/login')
@permission_required('ConfManage.views_policy', login_url='/noperm/')
def policy_iszmbie_check(request):
	if request.method == "GET":
		firewalllist = []
		for nxnode in Topo.nxtopology.nodes:
			if nxnode.type == "firewall":
				firewalllist.append({'name': nxnode.name})
		return render(request, 'policy/policy_iszmbie_check.html',{'firewalllist': firewalllist})
	elif request.method == "POST":
		policydiclist = []
		dev = request.POST.get('dev')
		for node in Topo.nxtopology.nodes:
			if dev == node.name:
				policydiclist = iszmbiepolicy(node)
				break
		return JsonResponse({'msg': '200', 'policy': policydiclist})


@login_required(login_url='/login')
@permission_required('ConfManage.views_policy', login_url='/noperm/')
def policy_regular_list(request):
	if request.method == "GET":
		regularlist = Applied_policy.objects.all()
		return render(request, 'policy/policy_regular_list.html',
		              {'regularlist': regularlist})
	elif request.method == "POST":
		option = request.POST.get('option')
		if option == '0':
			number = request.POST.get('number')
			Applied_policy.objects.get(id=number).delete()
			return JsonResponse({'msg': '200'})
		elif option == '1':
			name = request.POST.get('id')
			srcaddr = request.POST.get('srcaddr')
			dstaddr = request.POST.get('dstaddr')
			protocol = request.POST.get('protocol')
			port = request.POST.get('port')
			proposer = request.POST.get('proposer')
			if not is_ip(srcaddr) and not is_ip(dstaddr):
				return JsonResponse({'msg': "请输入合法IP地址~", "code": '502'})
			elif int(port) not in range(0, 65535):
				return JsonResponse({'msg': "请输入正确端口号，范围1-66535~", "code": '502'})
			elif " " in name:
				return JsonResponse({'msg': "名称中不能包含空格!!!", "code": '502'})
			else:
				try:
					Applied_policy.objects.create(name=name, srcaddr=srcaddr, dstaddr=dstaddr, protocol=protocol,
					                              port=port, proposer=proposer)
				except Exception as ex:
					print(ex)
				return JsonResponse({'msg': '200', "code": "200"})


@login_required(login_url='/login')
@permission_required('ConfManage.views_policy', login_url='/noperm/')
def policy_regular_check(request):
	if request.method == "GET":
		firewalllist = []
		for nxnode in Topo.nxtopology.nodes:
			if nxnode.type == "firewall":
				firewalllist.append({'name': nxnode.name})
		return render(request, 'policy/policy_regular_check.html', {'firewalllist': firewalllist})

	elif request.method == "POST":
		policydiclist = []
		dev = request.POST.get('dev')
		for node in Topo.nxtopology.nodes:
			if dev == node.name:
				policymiclist = regularcheck(node)
				for i in policymiclist:
					temppolicydic = {'dev': node.name,
									 'id': i.policyid,
									 'srceth': i.srceth,
									 'dsteth': i.dsteth,
									 'srcaddr': i.srcaddr,
									 'dstaddr': i.dstaddr,
									 'protocol': i.service['protocol'],
									 'port': i.service['port']}
					policydiclist.append(temppolicydic)
				break
		return JsonResponse({'msg': '200', 'policy': policydiclist})
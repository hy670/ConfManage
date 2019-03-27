#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
from importlib import reload
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ConfManage.utils.graph import usg100, f1030, nsg5000, iszmbiepolicy, regularcheck
from ConfManage.utils.is_ip import is_ip
from ConfManage.utils.topograph import Topo, searchpolicy
from ConfManage.models import Applied_policy, Network_Assets, Assets, Server_Assets, Line_Assets


@login_required(login_url='/login')
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
def policy_zone(request):
	if request.method == "GET":
		firewalllist = []
		nodeslist = []
		for nxnode in Topo.nxtopology.nodes:
			if nxnode.type == "firewall":
				firewalllist.append({'name': nxnode.name})
			nodeslist.append({'name': nxnode.name})
		return render(request, 'policy/policy_zone.html', {'nodes': nodeslist, 'firewalllist': firewalllist})
	elif request.method == "POST":
		nodelist = []
		if request.POST.get('op') == 'add_policy_zone':
			asset = request.POST.get('link_type')
			zone = request.POST.get('zone')
			dst_asset = request.POST.get('asset_name')
			netasset = Network_Assets.objects.get(hostname=asset)
			assets_type = ''
			net_asset = Network_Assets.objects.all()
			for asset in net_asset:
				if asset.hostname == dst_asset:
					assets_type = 'network'
			if not assets_type:
				ser_asset = Server_Assets.objects.all()
				for asset in ser_asset:
					if asset.hostname == dst_asset:
						assets_type = 'server'
			if not assets_type:
				line_asset = Line_Assets.objects.all()
				for asset in line_asset:
					if asset.line_name == dst_asset:
						assets_type = 'line'
			print(zone)
			print(assets_type)
			print(dst_asset)


@login_required(login_url='/login')
def policy_search(request):
	if request.method == "GET":
		return render(request, 'policy/policy_search.html')
	elif request.method == "POST":

		dev = request.POST.get('dev')
		srcaddr = request.POST.get('srcaddr')
		dstaddr = request.POST.get('dstaddr')
		protocol = request.POST.get('protocol')
		port = request.POST.get('port')
		if not protocol:
			protocol = '0'
		if not port:
			port = 0
		if not is_ip(srcaddr) and not is_ip(dstaddr):
			return JsonResponse({'msg': "请输入合法IP地址~", "code": '502'})
		elif int(port) not in range(0, 65535):
			return JsonResponse({'msg': "请输入正确端口号，范围1-66535~", "code": '502'})
		else:
			policydiclist = []
			tempdic = searchpolicy(srcaddr, dstaddr, protocol, port)
			if tempdic == False:
				return JsonResponse({'msg': "输入的地址不在网络范围内", "code": '502'})
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
			return JsonResponse({'policy': policydiclist, "code": '400'})


@login_required(login_url='/login')
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
def policy_iszmbie_check(request):
	if request.method == "GET":
		return render(request, 'policy/policy_iszmbie_check.html')
	elif request.method == "POST":
		policydiclist = []
		dev = request.POST.get('dev')
		if dev == 'usg':
			policydiclist = iszmbiepolicy(usg100)
			return JsonResponse({'msg': '200', 'policy': policydiclist})
		elif dev == 'f1030':
			policydiclist = iszmbiepolicy(f1030)
			return JsonResponse({'msg': '200', 'policy': policydiclist})
		elif dev == 'nsg':
			policydiclist = iszmbiepolicy(nsg5000)
			return JsonResponse({'msg': '200', 'policy': policydiclist})


@login_required(login_url='/login')
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
def policy_regular_check(request):
	if request.method == "GET":

		return render(request, 'policy/policy_regular_check.html')
	elif request.method == "POST":
		policydiclist = []
		dev = request.POST.get('dev')
		if dev == 'usg':
			policymiclist = regularcheck(usg100)
			for i in policymiclist:
				temppolicydic = {'dev': nsg5000.name, 'id': i.policyid, 'srceth': i.srceth, 'dsteth': i.dsteth,
				                 'srcaddr': i.srcaddr, 'dstaddr': i.dstaddr, 'protocol': i.service['protocol'],
				                 'port': i.service['port']}
				policydiclist.append(temppolicydic)
			return JsonResponse({'msg': '200', 'policy': policydiclist})
		elif dev == 'f1030':
			policymiclist = regularcheck(f1030)
			for i in policymiclist:
				temppolicydic = {'dev': nsg5000.name, 'id': i.policyid, 'srceth': i.srceth, 'dsteth': i.dsteth,
				                 'srcaddr': i.srcaddr, 'dstaddr': i.dstaddr, 'protocol': i.service['protocol'],
				                 'port': i.service['port']}
				policydiclist.append(temppolicydic)
			return JsonResponse({'msg': '200', 'policy': policydiclist})
		elif dev == 'nsg':
			policymiclist = regularcheck(nsg5000)
			for i in policymiclist:
				temppolicydic = {'dev': nsg5000.name, 'id': i.policyid, 'srceth': i.srceth, 'dsteth': i.dsteth,
				                 'srcaddr': i.srcaddr, 'dstaddr': i.dstaddr, 'protocol': i.service['protocol'],
				                 'port': i.service['port']}
				policydiclist.append(temppolicydic)
			return JsonResponse({'msg': '200', 'policy': policydiclist})

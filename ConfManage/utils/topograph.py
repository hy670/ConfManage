import IPy
import networkx
from ConfManage.utils import usg4000ep, f1030, nsg5000, devicebase
from ConfManage.utils.regularlist import RegularList
from ConfManage.models import *


def isnetaddr(addr):
	for netaddr in Topo.netaddrlist:
		if addr in IPy.IP(netaddr.netaddr):
			return True
	if IPy.IP(addr).iptype() == 'PUBLIC':
		return True
	elif addr == '0.0.0.0/0':
		return True
	else:
		return False

def iplocate(addr):
	for netaddr in Topo.netaddrlist:
		if addr in IPy.IP(netaddr.netaddr):
			return netaddr
	if IPy.IP(addr).iptype() == 'PUBLIC':
		return Topo.internet
	else:
		return False

def iszmbiepolicy(checkfirewall):
	zmbiepolicylist = []

	# 遍历需要检测防火墙的原子策略表
	for checkpoliy in checkfirewall.policymiclist:
		srcdev = ''
		dstdev = ''
		srcnetlist = []
		dstnetlist = []

		# 不对未初始化的安全域策略检查 设备互联地址
		if not isnetaddr(checkpoliy.srcaddr) or not isnetaddr(checkpoliy.dstaddr):
			continue

		if checkpoliy.srcaddr == '0.0.0.0/0':
			for port in checkfirewall.portlink:
				if checkpoliy.srceth in port:
					srcdev = port.split('-')[1]
			for i in Topo.nxtopology.nodes:
				if i.name == srcdev:
					srcnetlist = anychangenet(i, checkfirewall)
		else:
			srcnetlist.append(iplocate(checkpoliy.srcaddr))
		if checkpoliy.dstaddr == '0.0.0.0/0':
			for port in checkfirewall.portlink:
				if checkpoliy.dsteth in port:
					dstdev = port.split('-')[1]
			for i in Topo.nxtopology.nodes:
				if i.name == dstdev:
					dstnetlist = anychangenet(i, checkfirewall)
		else:
			dstnetlist.append(iplocate(checkpoliy.dstaddr))
		if len(dstnetlist) > 0 and len(srcnetlist) > 0:
			for srcnet in srcnetlist:
				for dstnet in dstnetlist:
					routelist = networkx.shortest_path(Topo.nxtopology, source=srcnet, target=dstnet)
					iscontent = 0
					# 遍历路径设备列表
					for i in range(len(routelist)):
						# 设备与策略主机一致跳过
						if routelist[i] == checkfirewall:
							continue
						# 如设备类型为防火墙
						elif routelist[i].type == 'firewall':
							# 根据上下游设备 确定检测策略经过本机的安全域或端口
							srceth = ''
							dsteth = ''
							for port in routelist[i].portlink:
								if routelist[i - 1].name in port:
									srceth = port.split('-')[0]
								if routelist[i + 1].name in port:
									dsteth = port.split('-')[0]
							# 遍历主机原子策略表，与经过的安全域策略比较是否有相应的策略
							for j in routelist[i].policymiclist:
								if j.srceth == srceth and j.dsteth == dsteth:
									iscontent = 1
									if IPy.IP(checkpoliy.srcaddr).overlaps(j.srcaddr) == 1 or IPy.IP(
											j.srcaddr).overlaps(
										checkpoliy.srcaddr) == 1:
										if IPy.IP(checkpoliy.dstaddr).overlaps(j.dstaddr) == 1 or IPy.IP(
												j.dstaddr).overlaps(
											checkpoliy.dstaddr) == 1:
											if checkpoliy.service['protocol'] == '0' or j.service['protocol'] == '0':
												#print("-----------------------匹配---------------------------------------")
												#print(routelist[i].name)
												#checkpoliy.printpolicymic()
												#j.printpolicymic()
												iscontent = 2
												break
											elif checkpoliy.service['port'] == j.service['port'] and checkpoliy.service['protocol'] == j.service[
												'protocol']:
												#print("-------------------------匹配-------------------------------------")
												#checkpoliy.printpolicymic()
												#j.printpolicymic()
												iscontent = 2
												break
							# 标识  表示 1= 相关安全域策略未匹配 2= 匹配（存在相对应的策略）
							if iscontent == 1:

								temppolicydic = {'dev': routelist[i].name, 'id': checkpoliy.policyid,
												 'srceth': checkpoliy.srceth,
												 'dsteth': checkpoliy.dsteth,
												 'srcaddr': checkpoliy.srcaddr,
												 'dstaddr': checkpoliy.dstaddr,
												 'protocol': checkpoliy.service['protocol'],
												 'port': checkpoliy.service['port']}
								zmbiepolicylist.append(temppolicydic)

	return zmbiepolicylist

def searchpolicy(srcaddr, dstaddr, protocol, service):
	searchpolicydic = {}
	dstnet = ""
	srcnet = ""
	if 	dstaddr == "0.0.0.0" or dstaddr == "0.0.0.0/0":
		dstnet = Topo.internet
	else:
		for i in Topo.netaddrlist:
			if 1 == IPy.IP(i.netaddr).overlaps(dstaddr):
				dstnet = i
				break

	if srcaddr == "0.0.0.0" or srcaddr == "0.0.0.0/0":
		srcnet = Topo.internet
	else:
		for i in Topo.netaddrlist:
			if 1 == IPy.IP(i.netaddr).overlaps(srcaddr):
				srcnet = i
				break
	# 根据策略的源区域和目的区域 确认策略路径 生成路径设备列表
	if not srcnet or not dstnet:
		return False
	else:
		routelist = networkx.shortest_path(Topo.nxtopology, source=srcnet, target=dstnet)
	# 遍历路径设备列表
	print(routelist)
	for i in range(len(routelist)):
		searchpolicylist = []
		if routelist[i].type == 'firewall':
			print(routelist[i].name)
			# 根据上下游设备 确定检测策略经过本机的安全域或端口
			srceth = ''
			dsteth = ''
			for port in routelist[i].portlink:
				if routelist[i - 1].name in port:
					srceth = port.split('-')[0]
				if routelist[i + 1].name in port:
					dsteth = port.split('-')[0]
			print(srceth)
			print(dsteth)
			# 遍历主机原子策略表，与经过的安全域策略比较是否有相应的策略
			for j in routelist[i].policymiclist:
				if j.srceth == srceth and j.dsteth == dsteth:
					if IPy.IP(srcaddr).overlaps(j.srcaddr) == 1 or IPy.IP(j.srcaddr).overlaps(
							srcaddr) == 1:
						if IPy.IP(dstaddr).overlaps(j.dstaddr) == 1 or IPy.IP(j.dstaddr).overlaps(
								dstaddr) == 1:
							if protocol == '0' or j.service['protocol'] == '0':
								# print("--------------------------------------------------------------")
								# checkpoliy.printpolicymic()
								searchpolicylist.append(j)
							elif protocol == j.service['protocol'] and service == j.service['port']:
								# print("--------------------------------------------------------------")
								# checkpoliy.printpolicymic()
								searchpolicylist.append(j)
		searchpolicydic.update({routelist[i].name: searchpolicylist})
	return searchpolicydic

def regularcheck(checkfirewall):

	policymiclist = checkfirewall.policymiclist.copy()
	regularpolicylist =[]

	for i in RegularList.regularlist:
		srcnet = iplocate(i['srcaddr'])
		dstnet = iplocate(i['dstaddr'])
		routelist = networkx.shortest_path(Topo.nxtopology, source=srcnet, target=dstnet)
		srceth = ''
		dsteth = ''

		for k in range(len(routelist)):
			if routelist[k] == checkfirewall:
				for port in checkfirewall.portlink:
					if routelist[k - 1].name in port:
						srceth = port.split('-')[0]
					if routelist[k + 1].name in port:
						dsteth = port.split('-')[0]

		if not srceth or not dsteth:
			continue
		else:
			for j in policymiclist:

				if j.srceth==srceth and j.dsteth==dsteth:
					if IPy.IP(i['srcaddr'])==IPy.IP(j.srcaddr) and IPy.IP(i['dstaddr']).overlaps(j.dstaddr) == 1:
							if i['protocol'] == j.service['protocol'] and i['port'] == j.service['port']:
								policymiclist.remove(j)

	return policymiclist

def anychangenet(srcdev, passdev):
	srcaddrlist = []

	for i in  Topo.netaddrlist:
		routelist = networkx.shortest_path(Topo.nxtopology, source=srcdev, target=i)
		if passdev not in routelist:
			srcaddrlist.append(i)
	routelist = networkx.shortest_path(Topo.nxtopology, source=srcdev, target=internet)
	if passdev not in routelist:
		srcaddrlist.append(Topo.internet)
	return srcaddrlist

class Topo:
	nodes =[]
	edges =[]
	netaddrlist = []
	internet =""
	nxtopology = networkx.Graph()
	netassets = Network_Assets.objects.filter(is_master=True)
	serassets = Server_Assets.objects.all()
	lineassets = Line_Assets.objects.filter(line_is_master=True)
	for netasset in netassets:
		asset = Assets.objects.get(id=netasset.assets_id)
		names = locals()
		if asset.assets_type == 'firewall':
			if asset.model =='USG4000EP':
				nxtopology.add_node(usg4000ep.USG4000EP(netasset.hostname))
			elif  asset.model =='NSG5500':
				nxtopology.add_node(nsg5000.NSG5000(netasset.hostname))
			elif asset.model == 'F1030':
				nxtopology.add_node(f1030.F1030(netasset.hostname))
		elif asset.assets_type == 'switch':
			nxtopology.add_node(devicebase.EthSW(netasset.hostname))
		elif asset.assets_type == 'route':
			nxtopology.add_node(devicebase.EthSW(netasset.hostname))
		nodes.append({'id': netasset.hostname, 'label': netasset.hostname})
	for serasset in serassets:
		netdev = devicebase.NetAddr(serasset.hostname, serasset.ip)
		netaddrlist.append(netdev)
		nxtopology.add_node(netdev)
		nodes.append({'id': serasset.hostname, 'label': serasset.hostname})
	for lineasset in lineassets:
		netdev = devicebase.NetAddr(lineasset.line_name, lineasset.line_ip)
		if netdev.netaddr == "0.0.0.0" or netdev.netaddr == "0.0.0.0/0":
			internet =netdev
		netaddrlist.append(netdev)
		nxtopology.add_node(netdev)
		nodes.append({'id': lineasset.line_name, 'label': lineasset.line_name})
	netedges =Network_Edges.objects.all()
	seredges = Server_Edges.objects.all()
	lineedges = Line_Edges.objects.all()
	for netedge in netedges:
		src = netedge.src.hostname
		dst = netedge.dst.hostname
		for nxnode in nxtopology.nodes:
			if nxnode.name == src:
				nxsrc = nxnode
			if nxnode.name == dst:
				nxdst = nxnode
		nxtopology.add_edge(nxsrc,nxdst)
		edges.append({'from': src, 'to': dst})
	for seredge in seredges:
		src = seredge.src.hostname
		dst = seredge.dst.hostname
		for nxnode in nxtopology.nodes:
			if nxnode.name == src:
				nxsrc = nxnode
			if nxnode.name == dst:
				nxdst = nxnode
		nxtopology.add_edge(nxsrc,nxdst)
		edges.append({'from': src, 'to': dst})
	for lineedge in lineedges:
		src = lineedge.src.hostname
		dst = lineedge.dst.line_name
		for nxnode in nxtopology.nodes:
			if nxnode.name == src:
				nxsrc = nxnode
			if nxnode.name == dst:
				nxdst = nxnode
		nxtopology.add_edge(nxsrc,nxdst)
		edges.append({'from': src, 'to': dst})






import IPy
import networkx
from ConfManage.utils import usg, f1030, nsg5000, devicebase
from ConfManage.utils.regularlist import RegularList
from ConfManage.models import *


class Topo:
	nodes =[]
	edges =[]
	netassets = Network_Assets.objects.filter(is_master=True)
	serassets = Server_Assets.objects.all()
	lineassets = Line_Assets.objects.filter(line_is_master=True)
	for netasset in netassets:
		nodes.append({'id': netasset.hostname, 'label': netasset.hostname})
	for serasset in serassets:
		nodes.append({'id': serasset.hostname, 'label': serasset.hostname})
	for lineasset in lineassets:
		nodes.append({'id': lineasset.line_name, 'label': lineasset.line_name})
	netedges =Network_Edges.objects.all()
	seredges = Server_Edges.objects.all()
	lineedges = Line_Edges.objects.all()
	for netedge in netedges:
		print(type(netedge.src))
		src = netedge.src.hostname
		dst = netedge.dst.hostname
		edges.append({'from': src, 'to': dst})
	for seredge in seredges:
		src = seredge.src.hostname
		dst = seredge.src.hostname
		edges.append({'from': src, 'to': dst})
	for lineedge in lineedges:
		src = lineedge.src.hostname
		dst = lineedge.dst.line_name
		edges.append({'from': src, 'to': dst})





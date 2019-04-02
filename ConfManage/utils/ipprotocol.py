# -*- coding:utf8 -*-


class IpProtocol:
	ipprotocallist =[]
	f = open('./ConfManage/utils/resource/ip-protocol', 'r', encoding="UTF-8")
	for line in f:
		key = line.strip().split(' ',2)
		if len(key)>2:
			ipprotocallist.append({'ipport':key[0],'name':str.upper(key[1]),})
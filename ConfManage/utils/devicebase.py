# -*- coding:utf8 -*-
"""
 创建防火墙策略列表 本机冗余策略检测
"""
import IPy




class NetAddr:
    def __init__(self, assetid, name, netaddr):
        self.assetid = assetid
        self.name = name
        self.type = 'netaddr'
        self.netaddr = netaddr


class EthSW:
    def __init__(self,assetid, name):
		self.assetid = assetid
		self.name = name
		self.type = 'SW'

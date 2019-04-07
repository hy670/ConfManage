#!/usr/bin/python

# -*- coding: utf-8 -*-
import threading
from ConfManage.utils import conf_bak
from ConfManage.utils.logger import logger
from ConfManage.models import Assets, Network_Assets


def crontab_bak():
	assets = Assets.objects.all()
	print("开始备份")
	for asset in assets:
		if str.lower(asset.manufacturer) == 'h3c' and asset.assets_type in ['friewall','switch','route']:
			net_asset = Network_Assets.objects.get(assets_id=asset.id)
			if net_asset.passwd and net_asset.username:
				bak_dev = conf_bak.H3cSW(net_asset.hostname,net_asset.ip,net_asset.port,net_asset.username,net_asset.passwd)
				bak_thread = threading.Thread(bak_dev.conf_bak())
			else:
				print("%s的用户名或密码不存在，取消备份", net_asset.hostname)

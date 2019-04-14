#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
from celery import task
from ConfManage.models import Assets,Network_Assets
from ConfManage.utils import conf_bak
from ConfManage.models import Conffile
from ConfManage.utils.logger import logger
import threading


@task
def cron_bak():
	assets = Assets.objects.all()
	logger.info("开始备份任务")
	for asset in assets:
		if str.lower(asset.manufacturer) == 'h3c' and asset.assets_type in ['firewall', 'switch', 'route']:
			net_asset = Network_Assets.objects.get(assets_id=asset.id)
			if net_asset.passwd and net_asset.username:
				bak_dev = conf_bak.H3cSW(net_asset.hostname, net_asset.ip, int(net_asset.port), net_asset.username,
										 net_asset.passwd)
				bak_thread = threading.Thread(bak_dev.conf_bak())
			else:
				logger.warn("%s-的用户名或密码不存在，取消备份", net_asset.hostname)
		elif str.lower(asset.manufacturer) == 'ruijie' and asset.assets_type in ['firewall', 'switch', 'route']:
			net_asset = Network_Assets.objects.get(assets_id=asset.id)
			if net_asset.passwd and net_asset.username:
				bak_dev = conf_bak.RuiJeiSW(net_asset.hostname, net_asset.ip, int(net_asset.port), net_asset.username,
											net_asset.passwd)
				bak_thread = threading.Thread(bak_dev.conf_bak())
			else:
				logger.warn("%s-的用户名或密码不存在，取消备份", net_asset.hostname)

@task
def file_clean():
	net_assets = Network_Assets.objects.all()
	for net_asset in net_assets:
		file_num = Conffile.objects.filter(network_assets_id=net_asset.id).count()
		if file_num>30:
			obj_list = Conffile.objects.filter(network_assets_id=net_asset.id).order_by('create_date')
			obj_list[30:].delete()
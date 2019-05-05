#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
from celery import task
from ConfManage.models import Assets,Network_Assets
from ConfManage.utils import conf_bak
from ConfManage.models import Conffile
from baseline.models import *
from ConfManage.utils.logger import logger
import threading

@task
def add():
	for i in range(0,30):
		print (i)
	return 100

@task
def check_conf(rules,assets):
	for asset in assets:
		try:
			netasset = Network_Assets.objects.get(assets_id=asset)
			conffile = Conffile.objects.get(network_assets_id=netasset.id)
			print(conffile.filename)
		except Exception as e:
			logger.warn(e)
	for rule in rules:
		try:
			check_group = check_group_mge.objects.filter(group_id=rule)
			grp_rel_list = check_grp_rel.objects.filter(group_id=rule)
		except Exception as e:
			logger.warn(e)
		for grp_rel in grp_rel_list:
			rule_manages = check_rule_manage.objects.filter(rule_id=grp_rel.rule_id)
			for rule_manage in rule_manages:
				try:
					print(rule_manage.rule_name)
					rule_contents = check_rule_content.objects.filter(rule_id=rule_manage.rule_id)
					for rule_content in rule_contents:
						print(rule_content.content_id)
				except Exception as e:
					logger.warn(e)





@task
def file_clean():
	net_assets = Network_Assets.objects.all()
	for net_asset in net_assets:
		file_num = Conffile.objects.filter(network_assets_id=net_asset.id).count()
		if file_num>30:
			obj_list = Conffile.objects.filter(network_assets_id=net_asset.id).order_by('create_date')
			obj_list[30:].delete()
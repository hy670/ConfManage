#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
import os
import re
import chardet
from celery import task
from ConfManage.models import Assets,Network_Assets
from ConfManage.utils import conf_bak
from ConfManage.models import Conffile
from baseline.models import *
from ConfManage.utils.logger import logger
import threading
from  djcelery.models import TaskMeta

@task(bind=True)
def add(self):
	print(self.request.id)
	for i in range(0,3):
		print (i)
	return 100

@task(bind=True)
def check_conf(self,rules,assets):
	print("开始任务 ID ："+self.request.id)
	for asset in assets:
		try:
			netasset = Network_Assets.objects.get(assets_id=asset)
			conffile = Conffile.objects.get(network_assets_id=netasset.id)
			filename = os.path.join(os.getcwd() + '/conffile/', conffile.filename)
			with open(filename, "rb") as f:
				data = f.read()
				encode = chardet.detect(data)
			f = open(filename, 'r', encoding=encode["encoding"])
		except Exception as e:
			logger.warn(e)
			task_assets_result.objects.create(asset_id=asset,task_id=self.request.id, result=1,result_des=e)
			continue

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
							if rule_content.spl_rule_cfg is not None:
								result = re.search(rule_content.rule_content,f.read())
								if (result.group('key')== "public"):
									print(netasset.hostname+"团体字为默认")
								else:
									print(netasset.hostname+"团体字为非默认")
								for result in result.groups():
									print(result)

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
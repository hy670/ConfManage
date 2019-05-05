#!/usr/bin/env python
# _#_ coding:utf-8 _*_
from django.shortcuts import render
from ConfManage.utils.logger import logger
from django.db import transaction
from baseline.models import *
from django.http import Http404
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse,HttpResponse
from ConfManage.utils.logger import logger
import json
from baseline import serializers as baselineserializers
from ConfManage import serializers as confmanageserializers
from ConfManage.models import Assets
from celery import task
from celery.registry import tasks as cTasks
from celery import registry
from celery.task.control import revoke
from celery.five import keys, items
from djcelery.models import PeriodicTask,CrontabSchedule,WorkerState,TaskState,IntervalSchedule
from baseline.tasks import *

def check_rule(request):
	if request.method == "GET":
		regexgrouplist = check_group_mge.objects.all()

		return render(request, 'baseline/RegexGroupLis.html', {"regexgrouplist": regexgrouplist})


def regex_group_detail(request, group_id):
	if request.method == "GET":
		group = check_group_mge.objects.get(group_id=group_id)
		group_rule_detail_list = check_grp_rel.objects.filter(group=group)
		rulelist = []
		for group_rule_detail in group_rule_detail_list:
			rule = group_rule_detail.rule
			rulelist.append(rule)
		return render(request, 'baseline/RegexGroupDetail.html', {'group': group, 'rulelist': rulelist})


def regex_rule_detail(request):
	if request.method == "GET":
		pass
		return render(request, 'baseline/RegexGroupDetail.html')
	elif request.method == "POST":
		rule_id = int(request.POST.get('rule_id'))
		try:
			rulecontentlist =[]
			rule = baselineserializers.RuleManageSerializer(check_rule_manage.objects.get(rule_id=rule_id)).data
			rulecontent = check_rule_content.objects.filter(rule_id=rule_id)
			for i in rulecontent:
				data = baselineserializers.RuleContentSerializer(i)
				rulecontentlist.append(data.data)
			return JsonResponse({'code': 400, 'rule':  rule, 'rulecontent':  rulecontentlist})
		except Exception as e:
			logger.warn("查询失败失败原因：%s", e)


		#return JsonResponse({'code':500,'rule': rule, 'rulecontent': rulecontent})




def regex_group_add(request):
	if request.method == "GET":

		return render(request, 'baseline/RegexGroupAdd.html')
	elif request.method == "POST":
		rule_list = json.loads(request.body)['rule_list']
		try:
			with transaction.atomic():
				groupmge_snippets = json.loads(request.body).copy()
				groupmge_snippets.pop('rule_list')
				groupemge_result =check_group_mge.objects.create(**groupmge_snippets)
				for rule in rule_list:
					rule_snippets =rule.copy()
					rule_snippets.pop('rule_content')
					rule_result = check_rule_manage.objects.create(**rule_snippets)
					for rulecontent in rule['rule_content']:
						rulecontent['rule'] = rule_result
						result = check_rule_content.objects.create(**rulecontent)

					check_grp_rel.objects.create(group=groupemge_result,rule=rule_result)
				return JsonResponse({"msg": "插入成功", "code": 400})
		except Exception as e:
			logger.warn("新增基线策略失败，失败原因%s",e)
			return JsonResponse({"msg":"插入失败","code":502})

def regex_task_add(request):
	if request.method == "GET":
		regexgrouplist = check_group_mge.objects.all()
		return render(request, 'baseline/RegexTaskAdd.html',{"regexgrouplist": regexgrouplist})
	elif request.method == "POST":
		op = json.loads(request.body)['op']
		if op == 'get_dev':
			try:
				assets = confmanageserializers.AssetsSerializer(Assets.objects.all(),many=True).data
			except Exception as e:
				logger.warn(e)
			return JsonResponse({"msg": "插入成功", "code": 400,'assets':assets})
		elif op == 'add_task':
			task = json.loads(request.body)['task']
			cron.check_conf(task['rule_list'],task['dev_list'])
			'''try:
				PeriodicTask.objects.create(name=task['task_name'],
				                            interval_id=request.POST.get('interval', None),
				                            task=request.POST.get('task', None),
				                            crontab_id=request.POST.get('crontab', None),
				                            args=request.POST.get('args', '[]'),
				                            kwargs=request.POST.get('kwargs', '{}'),
				                            queue=request.POST.get('queue', None),
				                            enabled=int(request.POST.get('enabled', 1)),
				                            expires=request.POST.get('expires', None)
				                            )
				return JsonResponse({"code": 200, "data": None, "msg": "添加成功"})
			except Exception as e:'''
			return JsonResponse({"code": 500,  "msg": "添加失败"})


#!/usr/bin/env python
# _#_ coding:utf-8 _*_
from django.shortcuts import render
from ConfManage.utils.logger import logger
from rest_framework import viewsets, permissions
from api import serializers
from baseline.models import *
from django.http import Http404
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
from ConfManage.utils.logger import logger
import json


def check_rule(request):
	if request.method == "GET":
		regexgrouplist = check_group_mge.objects.all()
		print(regexgrouplist)
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


def regex_group_add(request):
	if request.method == "GET":
		return render(request, 'baseline/RegexGroupAdd.html')
	elif request.method == "POST":
		rule_list = json.loads(request.body)['rule_list']
		print(rule_list)
		addgroup =check_group_mge.objects.create(group_name=json.loads(request.body)['group_name'],
									   group_des=json.loads(request.body)['group_des'])
		for rule in rule_list:
			ruleresult = check_rule_manage.objects.create(rule_name=rule['rule_name'],
														  rule_des=rule['rule_des'],
														  type=1,
														  rule_severity=int(rule['rule_severity']),
														  rule_standard=int(rule['rule_standard']),
														  )

			for rulecontent in rule['rule_content']:
				if rule['rule_standard'] == '0':
					result = check_rule_content.objects.create(
						rule_content=rulecontent['rule_content'],
						spl_rule_cfg=int(rulecontent['rule_cfg']),
						rule=ruleresult
					)

			check_grp_rel.objects.create(group=addgroup,rule=ruleresult)
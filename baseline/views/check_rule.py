#!/usr/bin/env python
# _#_ coding:utf-8 _*_
from django.shortcuts import render
from ConfManage.utils.logger import logger
from rest_framework import viewsets,permissions
from api import serializers
from baseline.models import *
from django.http import Http404
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
from ConfManage.utils.logger import logger


def check_rule(request):
	if request.method == "GET":
		regexgrouplist = check_group_mge.objects.all()
		print(regexgrouplist)
		return  render(request, 'baseline/RegexGroupLis.html',{"regexgrouplist":regexgrouplist} )

def regex_group_detail(request,group_id):
	if request.method == "GET":
		group = check_group_mge.objects.get(group_id=group_id)
		group_rule_detail_list = check_grp_rel.objects.filter(group=group)
		rulelist = []
		for group_rule_detail in group_rule_detail_list:
			rule = group_rule_detail.rule
			rulelist.append(rule)
		return  render(request, 'baseline/RegexGroupDetail.html',{'group':group,'rulelist':rulelist} )
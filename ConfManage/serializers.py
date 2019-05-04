#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
from rest_framework import serializers
from ConfManage.models import *
from baseline.models import *
from django.contrib.auth.models import Group, User


class LineAssetsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Line_Assets
		fields = ('id', 'line_name', 'line_ip', 'line_is_master')


class AssetsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Assets
		fields = ('id','assets_type', 'name', 'sn', 'buy_user', 'management_ip', 'manufacturer', 'model','mark', 'create_date', 'update_date')


class RuleContentSerializer(serializers.ModelSerializer):
	class Meta:
		model = check_rule_content
		fields = ('content_id', 'spl_rule_cfg', 'adv_rule_cfg', 'rule_relation',
				  'rule_content', 'match_content_type', 'getValue_compType',
				  'expression_compValue',
				  )

#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
from rest_framework import serializers
from baseline.models import *


class RuleManageSerializer(serializers.ModelSerializer):
	class Meta:
		model = check_rule_manage
		fields = ('rule_id', 'rule_name', 'rule_des', 'rule_severity',
				  'type', 'rule_standard', 'exec_method', 'file_path',
				  'check_content', 'command', 'support_firm', 'check_type',
				  'check_content_start', 'check_content_end',
				  'config_command', 'recover_command', 'creator', 'create_time')


class RuleContentSerializer(serializers.ModelSerializer):
	class Meta:
		model = check_rule_content
		fields = ('content_id', 'spl_rule_cfg', 'adv_rule_cfg', 'rule_relation',
				  'rule_content', 'match_content_type', 'getValue_compType',
				  'expression_compValue',
				  )

#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
from rest_framework import serializers
from ConfManage.models import *
from django.contrib.auth.models import Group,User


class LineAssetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Line_Assets
        fields = ('id','line_name','line_ip','line_is_master')
 




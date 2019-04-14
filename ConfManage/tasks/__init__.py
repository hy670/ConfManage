#!/usr/bin/env python
# _#_ coding:utf-8 _*_
'''
Django 版本大于等于1.7的时候，需要加上下面两句
import django
django.setup()
否则会抛出错误 django.core.exceptions.AppRegistryNotReady: Models aren't loaded yet.
'''
from __future__ import absolute_import
import django
django.setup()
from ConfManage.tasks.sched import *
from ConfManage.tasks.cron import *
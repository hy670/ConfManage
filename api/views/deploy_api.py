#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
from rest_framework import viewsets,permissions
from api import serializers
from ConfManage.models import *
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
#from OpsManage.tasks.deploy import recordProject
from django.contrib.auth.decorators import permission_required
from rest_framework import generics
from django.db.models import Q 

    
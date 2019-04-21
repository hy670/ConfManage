#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
from rest_framework import viewsets,permissions
from api import serializers
from ConfManage.models import *
from rest_framework import status
from django.http import Http404
from django.contrib.auth.models import Group
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
#from OpsManage.tasks.assets import recordAssets
from django.contrib.auth.decorators import permission_required
from ConfManage.utils.logger import logger
from django.http import JsonResponse



    
@api_view(['GET', 'POST' ])
@permission_required('ConfManage.add_group',raise_exception=True)
def group_list(request,format=None):
    """
    List all order, or create a server assets order.
    """
    print("diayong group list")
    if not  request.user.has_perm('ConfManage.read_group'):
        return Response(status=status.HTTP_403_FORBIDDEN)     
    if request.method == 'GET':      
        snippets = Group.objects.all()
        serializer = serializers.GroupSerializer(snippets, many=True)
        return Response(serializer.data)     
    elif request.method == 'POST':
        if not  request.user.has_perm('ConfManage.change_group'):
            return Response(status=status.HTTP_403_FORBIDDEN)         
        serializer = serializers.GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            #recordAssets.delay(user=str(request.user),content="添加用户组：{group_name}".format(group_name=request.data.get("name")),type="group",id=serializer.data.get('id'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('ConfManage.change_group',raise_exception=False)
def group_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """    
    try:
        snippet = Group.objects.get(id=id)
    except Group.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = serializers.GroupSerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT':
        serializer = serializers.GroupSerializer(snippet, data=request.data)
        old_name = snippet.name
        if serializer.is_valid():
            serializer.save()
            #recordAssets.delay(user=str(request.user),content="修改用户组名称：{old_name} -> {group_name}".format(old_name=old_name,group_name=request.data.get("name")),type="group",id=id)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('ConfManage.delete_group'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        #recordAssets.delay(user=str(request.user),content="删除用户组：{group_name}".format(group_name=snippet.name),type="group",id=id)
        return Response(status=status.HTTP_204_NO_CONTENT)     


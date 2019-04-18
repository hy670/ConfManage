#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from ConfManage.utils.logger import logger


@login_required()
def baseline_list(request):
    if request.method == "GET":
        pass
        return render(request,'baseline/baseline_list.html')
    elif request.method == "POST":
        return  JsonResponse({"code":500,"data":None,"msg":"不支持的HTTP操作"})

@login_required()
def baseline_manage(request):
    if request.method == "GET":
        pass
        return render(request,'baseline/baseline_manage.html')
    elif request.method == "POST":
        return  JsonResponse({"code":500,"data":None,"msg":"不支持的HTTP操作"})
    
    

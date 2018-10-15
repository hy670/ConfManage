#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
from django.http import JsonResponse
from django.shortcuts import render
from ConfManage.utils.graph import usg100,f1030,nsg5000,searchpolicy
from ConfManage.utils.is_ip import is_ip




def policy_list(request):
    if request.method == "GET":
        return render(request,'policy/policy_list.html')
    elif request.method == "POST":
        policydiclist =[]
        dev =request.POST.get('dev')
        if dev =='usg':
            for i in usg100.policymiclist:
                temppolicydic ={'dev':usg100.name,'id':i.policyid,'srceth':i.srceth,'dsteth':i.dsteth,
                                'srcaddr':i.srcaddr,'dstaddr':i.dstaddr,'protocol':i.service['protocol'],
                                'port':i.service['port']}
                policydiclist.append(temppolicydic)
            return JsonResponse({'msg':'200','policy':policydiclist})
        elif dev =='f1030':
            for i in f1030.policymiclist:
                temppolicydic = {'dev': f1030.name, 'id': i.name, 'srceth': i.srceth, 'dsteth': i.dsteth,
                                 'srcaddr': i.srcaddr, 'dstaddr': i.dstaddr, 'protocol': i.service['protocol'],
                                 'port': i.service['port']}
                policydiclist.append(temppolicydic)
            return JsonResponse({'msg': '200', 'policy': policydiclist})
        elif dev =='nsg':
            for i in nsg5000.policymiclist:
                temppolicydic = {'dev': nsg5000.name, 'id': i.name, 'srceth': i.srceth, 'dsteth': i.dsteth,
                                 'srcaddr': i.srcaddr, 'dstaddr': i.dstaddr, 'protocol': i.service['protocol'],
                                 'port': i.service['port']}
                policydiclist.append(temppolicydic)
            return JsonResponse({'msg': '200', 'policy': policydiclist})


def policy_search(request):
    if request.method == "GET":
        return render(request, 'policy/policy_search.html')
    elif request.method == "POST":
        srcaddr = request.POST.get('srcaddr')
        dstaddr = request.POST.get('dstaddr')
        protocol = request.POST.get('protocol')
        port = request.POST.get('port')
        if not port:
            port = -1

        if not is_ip(srcaddr) and not is_ip(dstaddr):
            return JsonResponse({'msg':"请输入合法IP地址~", "code":'502'})
        elif int(port) not in range(-1,65535):
            return JsonResponse({'msg':"请输入正确端口号，范围1-66535~", "code":'502'})
        else:
            policydiclist = []
            if port == -1:
                port = 'any'
            tempdic=searchpolicy(srcaddr,dstaddr,port)
            for key in tempdic:
                if len(tempdic[key]) > 0:
                    for i in tempdic[key]:
                        temppolicydic = {'dev': key, 'id': i.name, 'srceth': i.srceth, 'dsteth': i.dsteth,
                                        'srcaddr': i.srcaddr, 'dstaddr': i.dstaddr, 'protocol': i.service['protocol'],
                                        'port': i.service['port']}
                        policydiclist.append(temppolicydic)
            return JsonResponse({'policy':policydiclist, "code":'400'})





#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
import MySQLdb
from celery import task
from ConfManage.utils import base
import time

@task 
def expireAssets(**kw):   
    pass

@task

def add():

    for i in range(30):

       print (i)

       time.sleep(1)

    return True
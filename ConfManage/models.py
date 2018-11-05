#!/usr/bin/env python  
# _#_ coding:utf-8 _*_

import sys
from imp import reload

from django.db import models

reload(sys)



class Assets(models.Model):
    assets_type_choices = (
                          ('server',u'服务器'),
                          ('vmser',u'虚拟机'),
                          ('switch',u'交换机'),
                          ('route',u'路由器'),
                          ('firewall',u'防火墙'),
                          ('storage',u'存储设备'),
                          )
    assets_type = models.CharField(choices=assets_type_choices,max_length=100,default='server',verbose_name='资产类型')
    name = models.CharField(max_length=100,verbose_name='资产编号',unique=True)
    sn =  models.CharField(max_length=100,verbose_name='设备序列号',blank=True,null=True)
    buy_time = models.DateField(blank=True,null=True,verbose_name='购买时间')
    expire_date = models.DateField(u'过保修期',null=True, blank=True)
    buy_user = models.SmallIntegerField(blank=True,null=True,verbose_name='购买人')
    management_ip = models.GenericIPAddressField(u'管理IP',blank=True,null=True)
    manufacturer = models.CharField(max_length=100,blank=True,null=True,verbose_name='制造商')
    provider = models.CharField(max_length=100,blank=True,null=True,verbose_name='供货商')
    model = models.CharField(max_length=100,blank=True,null=True,verbose_name='资产型号')
    mark = models.TextField(blank=True,null=True,verbose_name='资产标示')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'confmanage_assets'
        permissions = (
            ("can_read_assets", "读取资产权限"),
            ("can_change_assets", "更改资产权限"),
            ("can_add_assets", "添加资产权限"),
            ("can_delete_assets", "删除资产权限"),
            ("can_dumps_assets", "导出资产权限"),
        ) 
        verbose_name = '总资产表'  
        verbose_name_plural = '总资产表'  


class Server_Assets(models.Model): 
    assets = models.OneToOneField('Assets',on_delete=models.CASCADE)
    ip = models.CharField(max_length=100,unique=True,blank=True,null=True)  
    hostname = models.CharField(max_length=100,blank=True,null=True)  
    username = models.CharField(max_length=100,blank=True,null=True)  
    passwd = models.CharField(max_length=100,blank=True,null=True)  
    sudo_passwd = models.CharField(max_length=100,blank=True,null=True)
    keyfile =  models.SmallIntegerField(blank=True,null=True)#FileField(upload_to = './upload/key/',blank=True,null=True,verbose_name='密钥文件')
    port = models.DecimalField(max_digits=6,decimal_places=0,blank=True,null=True)
    line = models.SmallIntegerField(blank=True,null=True)
    cpu = models.CharField(max_length=100,blank=True,null=True)
    cpu_number = models.SmallIntegerField(blank=True,null=True)
    vcpu_number = models.SmallIntegerField(blank=True,null=True)
    cpu_core = models.SmallIntegerField(blank=True,null=True)
    disk_total = models.CharField(max_length=100,blank=True,null=True)
    ram_total= models.IntegerField(blank=True,null=True)
    kernel = models.CharField(max_length=100,blank=True,null=True)
    selinux = models.CharField(max_length=100,blank=True,null=True)
    swap = models.CharField(max_length=100,blank=True,null=True)
    raid = models.SmallIntegerField(blank=True,null=True)
    system = models.CharField(max_length=100,blank=True,null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    '''自定义添加只读权限-系统自带了add change delete三种权限'''
    class Meta:
        db_table = 'confmanage_server_assets'
        permissions = (
            ("can_read_server_assets", "读取服务器资产权限"),
            ("can_change_server_assets", "更改服务器资产权限"),
            ("can_add_server_assets", "添加服务器资产权限"),
            ("can_delete_server_assets", "删除服务器资产权限"),            
        )
        verbose_name = '服务器资产表'  
        verbose_name_plural = '服务器资产表' 


class Network_Assets(models.Model):
    assets = models.OneToOneField('Assets',on_delete=models.CASCADE)
    bandwidth =  models.CharField(max_length=100,blank=True,null=True,verbose_name='背板带宽') 
    ip = models.CharField(unique=True,max_length=100,blank=True,null=True,verbose_name='管理ip')
    username = models.CharField(max_length=100,blank=True,null=True)
    passwd = models.CharField(max_length=100,blank=True,null=True) 
    sudo_passwd = models.CharField(max_length=100,blank=True,null=True) 
    port = models.DecimalField(max_digits=6,decimal_places=0,blank=True,null=True)    
    port_number = models.SmallIntegerField(blank=True,null=True,verbose_name='端口个数')
    firmware =  models.CharField(max_length=100,blank=True,null=True,verbose_name='固件版本')
    cpu = models.CharField(max_length=100,blank=True,null=True,verbose_name='cpu型号')
    stone = models.CharField(max_length=100,blank=True,null=True,verbose_name='内存大小')
    configure_detail = models.TextField(max_length=100,blank=True,null=True,verbose_name='配置说明')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)    
    class Meta:
        db_table = 'confmanage_network_assets'
        permissions = (
            ("can_read_network_assets", "读取网络资产权限"),
            ("can_change_network_assets", "更改网络资产权限"),
            ("can_add_network_assets", "添加网络资产权限"),
            ("can_delete_network_assets", "删除网络资产权限"), 
        ) 
        verbose_name = '网络资产表'  
        verbose_name_plural = '网络资产表' 

    
class Disk_Assets(models.Model):      
    assets = models.ForeignKey('Assets',on_delete=models.CASCADE)
    device_volume =  models.CharField(max_length=100,blank=True,null=True,verbose_name='硬盘容量') 
    device_status =  models.CharField(max_length=100,blank=True,null=True,verbose_name='硬盘状态')
    device_model = models.CharField(max_length=100,blank=True,null=True,verbose_name='硬盘型号')
    device_brand = models.CharField(max_length=100,blank=True,null=True,verbose_name='硬盘生产商')
    device_serial =  models.CharField(max_length=100,blank=True,null=True,verbose_name='硬盘序列号')
    device_slot = models.SmallIntegerField(blank=True,null=True,verbose_name='硬盘插槽')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)   
    class Meta:
        db_table = 'confmanage_disk_assets'
        permissions = (
            ("can_read_disk_assets", "读取磁盘资产权限"),
            ("can_change_disk_assets", "更改磁盘资产权限"),
            ("can_add_disk_assets", "添加磁盘资产权限"),
            ("can_delete_disk_assets", "删除磁盘资产权限"),             
        ) 
        unique_together = (("assets", "device_slot"))
        verbose_name = '磁盘资产表'  
        verbose_name_plural = '磁盘资产表'  


        

        

              

                  


                
class Line_Assets(models.Model):   
    line_name = models.CharField(max_length=100,unique=True)     
    '''自定义权限'''
    class Meta:
        db_table = 'opsmanage_line_assets'
        permissions = (
            ("can_read_line_assets", "读取出口线路资产权限"),
            ("can_change_line_assetss", "更改出口线路资产权限"),
            ("can_add_line_assets", "添加出口线路资产权限"),
            ("can_delete_line_assets", "删除出口线路资产权限"),             
        )
        verbose_name = '出口线路资产表'  
        verbose_name_plural = '出口线路资产表' 
        





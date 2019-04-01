from __future__ import unicode_literals

from django.db import models
# from OpsManage.models import Project_Config,DataBase_Server_Config
import sys


class Applied_policy(models.Model):
	name = models.CharField(max_length=100, verbose_name='策略名称', unique=True)
	srcaddr = models.CharField(max_length=15, verbose_name='源地址', blank=True, null=True)
	dstaddr = models.CharField(max_length=15, verbose_name='源地址', blank=True, null=True)
	protocol = models.IntegerField(blank=True, null=True, verbose_name='协议')
	port = models.IntegerField(blank=True, null=True, verbose_name='端口')
	proposer = models.CharField(max_length=100, null=True, verbose_name='申请人')
	create_date = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'confmanage_Applied_policy'
		permissions = (
			("can_read_policy", "读取策略权限"),

			("can_change_policy", "更改策略权限"),
			("can_add_policy", "添加策略权限"),
			("can_delete_policy", "删除策略权限"),
			("can_dumps_policy", "导出策略权限"),
		)
		verbose_name = '已申请策略表'
		verbose_name_plural = '已申请总策略表'


class Assets(models.Model):
	assets_type_choices = (
		('server', u'服务器'),
		('vmser', u'虚拟机'),
		('switch', u'交换机'),
		('route', u'路由器'),
		('firewall', u'防火墙'),
		('storage', u'存储设备'),
		('line', u'线路资源')
	)
	assets_type = models.CharField(choices=assets_type_choices, max_length=100, default='server', verbose_name='资产类型')
	name = models.CharField(max_length=100, verbose_name='资产编号', unique=True)
	sn = models.CharField(max_length=100, verbose_name='设备序列号', blank=True, null=True)
	buy_user = models.SmallIntegerField(blank=True, null=True, verbose_name='购买人')
	management_ip = models.GenericIPAddressField(u'管理IP', blank=True, null=True)
	manufacturer = models.CharField(max_length=100, blank=True, null=True, verbose_name='制造商')
	model = models.CharField(max_length=100, blank=True, null=True, verbose_name='资产型号')
	mark = models.TextField(blank=True, null=True, verbose_name='资产标示')
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
	assets = models.OneToOneField('Assets', on_delete=models.CASCADE)
	ip = models.CharField(max_length=100, unique=True, blank=True, null=True)
	hostname = models.CharField(max_length=100, blank=True, null=True)
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
	assets = models.OneToOneField('Assets', on_delete=models.CASCADE)
	hostname = models.CharField(max_length=100, blank=True, null=True)
	ip = models.CharField( max_length=100, blank=True, null=True, verbose_name='管理ip')
	username = models.CharField(max_length=100, blank=True, null=True)
	passwd = models.CharField(max_length=100, blank=True, null=True)
	sudo_passwd = models.CharField(max_length=100, blank=True, null=True)
	port = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)
	port_number = models.SmallIntegerField(blank=True, null=True, verbose_name='端口个数')
	configure_detail = models.TextField(max_length=100, blank=True, null=True, verbose_name='配置说明')
	is_master = models.BooleanField(default=True, verbose_name="是否主设备")
	create_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'confmanage_network_assets'
		unique_together = ('ip', 'is_master')
		permissions = (
			("can_read_network_assets", "读取网络资产权限"),
			("can_change_network_assets", "更改网络资产权限"),
			("can_add_network_assets", "添加网络资产权限"),
			("can_delete_network_assets", "删除网络资产权限"),
		)
		verbose_name = '网络资产表'
		verbose_name_plural = '网络资产表'


class Line_Assets(models.Model):
	line_name = models.CharField(max_length=100, unique=True)
	line_ip = models.CharField(max_length=100, blank=True, null=True, verbose_name='IP地址')
	line_is_master = models.BooleanField(default=True, verbose_name="是否主设备")
	'''自定义权限'''

	class Meta:
		db_table = 'confmanage_line_assets'
		permissions = (
			("can_read_line_assets", "读取出口线路资产权限"),
			("can_change_line_assetss", "更改出口线路资产权限"),
			("can_add_line_assets", "添加出口线路资产权限"),
			("can_delete_line_assets", "删除出口线路资产权限"),
		)
		verbose_name = '外联线路资产表'
		verbose_name_plural = '外联线路资产表'


class Conffile(models.Model):
	network_assets = models.ForeignKey('Network_Assets',on_delete=models.CASCADE)
	filename = models.TextField(max_length=150, blank=True, null=True, verbose_name='文件名称')
	file_detail = models.TextField(max_length=200, blank=True, null=True, verbose_name='文件说明')
	create_date = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'confmanage_conffile'
		permissions = (
			("can_read_conffile", "读取网络配置文件"),
			("can_change_conffile", "更改网络配置文件"),
			("can_add_conffile", "添加网络配置文件"),
			("can_delete_conffile", "删除网络配置文件"),
		)
		verbose_name = '网络配置文件表'
		verbose_name_plural = '网络配置文件表'


class Edges(models.Model):
	edges_type_choices = (
		('server', u'服务器'),
		('net', u'网络设备'),
		('line', u'线路'),
	)
	edges_type = models.CharField(choices=edges_type_choices, max_length=100, default='net', verbose_name='链路类型')
	create_date = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'confmanage_edges'
		permissions = (
			("can_read_edges", "读取链路信息"),
			("can_change_edges", "更改链路"),
			("can_add_edges", "添加链路"),
			("can_delete_edges", "删除链路"),
		)
		verbose_name = '链路配置表'
		verbose_name_plural = '链路配置表'


class Server_Edges(models.Model):
	Edges = models.OneToOneField('Edges', on_delete=models.CASCADE)
	src =  models.ForeignKey('Network_Assets',on_delete=models.CASCADE)
	dst = models.ForeignKey('Server_Assets',on_delete=models.CASCADE)
	create_date = models.DateTimeField(auto_now_add=True)
	'''自定义添加只读权限-系统自带了add change delete三种权限'''

	class Meta:
		db_table = 'confmanage_server_edges'
		unique_together = ('src', 'dst')
		permissions = (
			("can_read_server_edges", "读取服务器链路"),
			("can_change_server_edges", "更改服务器链路"),
			("can_add_server_edges", "添加服务器链路"),
			("can_delete_server_edges", "删除服务器链路"),
		)
		verbose_name = '服务器链路表'
		verbose_name_plural = '服务器链路表'


class Network_Edges(models.Model):
	Edges = models.OneToOneField('Edges', on_delete=models.CASCADE)
	src =  models.ForeignKey('Network_Assets',on_delete=models.CASCADE,related_name='src')
	dst = models.ForeignKey('Network_Assets',on_delete=models.CASCADE,related_name='dst')
	create_date = models.DateTimeField(auto_now_add=True)
	'''自定义添加只读权限-系统自带了add change delete三种权限'''

	class Meta:
		db_table = 'confmanage_network_edges'
		unique_together = ('src', 'dst')
		permissions = (
			("can_read_network_edges", "读取网络链路"),
			("can_change_network_edges", "更改网络链路"),
			("can_add_network_edges", "添加网络链路"),
			("can_delete_network_edges", "删除网络链路"),
		)
		verbose_name = '网络链路表'
		verbose_name_plural = '网络链路表'


class Line_Edges(models.Model):
	Edges = models.OneToOneField('Edges', on_delete=models.CASCADE)
	src =  models.ForeignKey('Network_Assets',on_delete=models.CASCADE)
	dst = models.ForeignKey('Line_Assets',on_delete=models.CASCADE)
	create_date = models.DateTimeField(auto_now_add=True)
	'''自定义添加只读权限-系统自带了add change delete三种权限'''

	class Meta:
		db_table = 'confmanage_line_edges'
		unique_together = ('src', 'dst')
		permissions = (
			("can_read_line_edges", "读取线路链路"),
			("can_change_line_edges", "更改线路链路"),
			("can_add_line_edges", "添加线路链路"),
			("can_delete_line_edges", "删除线路链路"),
		)
		verbose_name = '线路链路表'
		verbose_name_plural = '线路链路表'
class Firewall_Policy_Zone(models.Model):
	Network_Assets = models.ForeignKey('Network_Assets', on_delete=models.CASCADE)
	zone = models.CharField(max_length=100, blank=True, null=True)
	assets_type = models.CharField(max_length=100, blank=True, null=True)
	assets_name = models.CharField(max_length=100, blank=True, null=True)
	create_date = models.DateTimeField(auto_now_add=True)
	'''自定义添加只读权限-系统自带了add change delete三种权限'''

	class Meta:
		db_table = 'confmanage_firewall_policy_zone'
		unique_together = ('zone', 'assets_name')
		permissions = (
			("can_read_firewall_policy_zone", "读取防火墙安全域列表"),
			("can_change_firewall_policy_zone", "更改防火墙安全域列表"),
			("can_add_firewall_policy_zone", "添加防火墙安全域列表"),
			("can_delete_firewall_policy_zone", "删除防火墙安全域列表"),
		)
		verbose_name = '防火墙安全域列表'
		verbose_name_plural = '防火墙安全域列表'

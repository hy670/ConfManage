from django.db import models

# Create your models here.


class check_rule_devseries(models.Model):
	rule_id = models.ForeignKey('check_rule_manage', on_delete=models.CASCADE)
	device_series_id = models.BigIntegerField()
	class Meta:
		db_table = 'baseline_check_rule_devseries'
		permissions = (
			("can_read_policy", "读取策略权限"),
			("can_change_policy", "更改策略权限"),
			("can_add_policy", "添加策略权限"),
			("can_delete_policy", "删除策略权限"),
			("can_dumps_policy", "导出策略权限"),
		)
		verbose_name = '已申请策略表'
		verbose_name_plural = '已申请总策略表'

class check_rule_manage(models.Model):
	rule_id = models.IntegerField(primary_key=True)
	rule_name = models.CharField(max_length=64)
	rule_des = models.CharField(max_length=256)
	rule_severity = models.SmallIntegerField()
	type = models.SmallIntegerField()
	rule_standard = models.SmallIntegerField(blank=True, null=True)
	exec_method = models.SmallIntegerField(blank=True, null=True)
	file_path = models.CharField(max_length=256,blank=True, null=True)
	check_content = models.SmallIntegerField(blank=True, null=True)
	command = models.CharField(max_length=4096,blank=True, null=True)
	support_firm = models.CharField(max_length=256,blank=True, null=True)
	check_type = models.SmallIntegerField(blank=True, null=True)
	check_content_start = models.TextField(blank=True, null=True)
	check_content_end = models.TextField(blank=True, null=True)
	config_command = models.TextField(blank=True, null=True)
	recover_command = models.TextField(blank=True, null=True)
	creator = models.CharField(max_length=64,blank=True, null=True)
	create_time = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'baseline_check_rule_manage'
		permissions = (
			("can_read_policy", "读取策略权限"),

			("can_change_policy", "更改策略权限"),
			("can_add_policy", "添加策略权限"),
			("can_delete_policy", "删除策略权限"),
			("can_dumps_policy", "导出策略权限"),
		)
		verbose_name = '已申请策略表'
		verbose_name_plural = '已申请总策略表'


class check_rule_content(models.Model):
	content_id = models.IntegerField(primary_key=True)
	rule_id = models.ForeignKey('check_rule_manage', on_delete=models.CASCADE)
	# 规则类型 简单匹配 高级匹配 取值(1:模糊匹配，2:模糊不匹配，3：精确匹配：4：精确不匹配）
	spl_rule_cfg = models.SmallIntegerField()
	adv_rule_cfg = models.SmallIntegerField()
	# rule 多条 conten 之间的关系 取值（0：OR ,1:?,2:?)
	rule_relation = models.SmallIntegerField()
	# 规则内容
	rule_content = models.TextField(blank=True, null=True)
	# 匹配类型 取值（1：全部不包含，2：包含其中之一）
	match_content_type = models.SmallIntegerField(blank=True, null=True)
	# 提取值的对比方式
	getValue_compType = models.SmallIntegerField(blank=True, null=True)
	# 提取值的对比值
	expression_compValue = models.CharField(max_length=256,blank=True, null=True)

	class Meta:
		db_table = 'baseline_check_rule_content'
		permissions = (
			("can_read_policy", "读取策略权限"),

			("can_change_policy", "更改策略权限"),
			("can_add_policy", "添加策略权限"),
			("can_delete_policy", "删除策略权限"),
			("can_dumps_policy", "导出策略权限"),
		)
		verbose_name = '已申请策略表'
		verbose_name_plural = '已申请总策略表'

class check_group_mge(models.Model):
	group_id = models.IntegerField(primary_key=True)
	group_name = models.CharField(max_length=64)
	group_des = models.CharField(max_length=256)
	type = models.SmallIntegerField()
	activate = models.SmallIntegerField()
	version = models.CharField(max_length=64,blank=True, null=True)
	component_name = models.CharField(max_length=64,blank=True, null=True)
	creator = models.CharField(max_length=64,blank=True, null=True)
	create_time = models.DateTimeField(auto_now_add=True,blank=True, null=True)

	class Meta:
		db_table = 'baseline_check_group_mge'
		permissions = (

		)
		verbose_name = ''
		verbose_name_plural = ''

class check_grp_rel(models.Model):
	rg_relation_id = models.IntegerField(primary_key=True)
	group = models.ForeignKey("check_group_mge",on_delete=models.CASCADE)
	rule = models.ForeignKey("check_rule_manage",on_delete=models.CASCADE)

	class Meta:
		db_table = 'baseline_check_grp_rel'
		permissions = (
		)
		verbose_name = ''
		verbose_name_plural = ''

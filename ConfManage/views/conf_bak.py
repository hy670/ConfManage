import time
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
import threading
from ConfManage.utils import conf_bak
from ConfManage.utils.logger import logger
from ConfManage.models import Assets, Network_Assets

try:
	# 实例化调度器
	scheduler = BackgroundScheduler()
	# 调度器使用DjangoJobStore()
	scheduler.add_jobstore(DjangoJobStore(), "default")

	# 'cron'方式循环，周一到周五，每天9:30:10执行,id为工作ID作为标记
	#@register_job(scheduler, 'cron', day_of_week='mon-fri', hour='9', minute='30', second='10', id='task_time')
	@register_job(scheduler, "interval", seconds=60)  # 用interval方式循环，每一秒执行一次
	def test_job():
		assets = Assets.objects.all()
		print("开始备份")
		for asset in assets:
			if str.lower(asset.manufacturer) == 'h3c' and asset.assets_type in ['firewall', 'switch', 'route']:
				net_asset = Network_Assets.objects.get(assets_id=asset.id)
				if net_asset.passwd and net_asset.username:
					bak_dev = conf_bak.H3cSW(net_asset.hostname, net_asset.ip, net_asset.port, net_asset.username,
											 net_asset.passwd)
					bak_thread = threading.Thread(bak_dev.conf_bak())
				else:
					print(net_asset.hostname+"-的用户名或密码不存在，取消备份", )


	# 监控任务
	register_events(scheduler)
	# 调度器开始
	scheduler.start()
except Exception as e:
	print(e)
# 报错则调度器停止执行

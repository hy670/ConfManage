#!/usr/bin/python

# -*- coding: utf-8 -*-

import re
import paramiko
import time,datetime
import threading
import chardet
import xlwt,xlrd
from ConfManage.utils.logger import logger


class RuiJeiSW:

	def __init__(self, hostname, ip, port, user, password):
		self.hostname = hostname
		self.ip = ip
		self.port = port
		self.user = user
		self.password = password
		self.client = None
		self.ssh_connect = None

	def new_ssh_connect(self):
		self.client = paramiko.SSHClient()
		self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		try:
			self.client.connect(self.ip, self.port, self.user, self.password, timeout=5)
			self.ssh_connect = self.client.invoke_shell()
		except Exception as e:
			logger.info("%s SSH 连接失败，失败原因：%s", self.hostname, e)
			exit()

	def del_ssh_connect(self):
		self.client.close()
		logger.info("%s SSH 连接关闭",self.hostname)

	def to_enable(self):
		self.ssh_connect.send('enable\n')
		time.sleep(1)
		out = self.ssh_connect.recv(1024).decode()
		if "Password:" in out:
			self.ssh_connect.send('wangluo123\n')
			time.sleep(1)
			out = self.ssh_connect.recv(1024).decode()
			if "Password:" in out:
				logger.info("进入enable 失败，请检查密码是否正确")
				exit()
			elif "Ruijie#" in out:
				logger.info("进入enable模式")

	def show_run(self):
		out = self.ssh_connect.recv(1024).decode()
		self.ssh_connect.send('ls \n')
		time.sleep(1)
		out = self.ssh_connect.recv(1024).decode()
		conf = out
		while "Ruijie#" not in out:
			self.ssh_connect.send('  ')
			out = self.ssh_connect.recv(1024).decode()
			conf = conf + out

	def show_mac(self):
		self.ssh_connect.send('show mac \n')
		time.sleep(1)
		out = self.ssh_connect.recv(1024).decode()
		conf = out
		while "Ruijie#" not in out:
			self.ssh_connect.send('  ')
			out = self.ssh_connect.recv(1024).decode()
			conf = conf + out
		print(conf)

	def show_arp(self):
		self.ssh_connect.send('show arp \n')
		time.sleep(1)
		out = self.ssh_connect.recv(1024).decode()
		conf = out
		while "Ruijie#" not in out:
			self.ssh_connect.send('  ')
			out = self.ssh_connect.recv(1024).decode()
			conf = conf + out
		print(conf)

	def conf_bak(self):
		self.new_ssh_connect()
		out = self.ssh_connect.recv(1024).decode()
		self.to_enable()
		logger.info("????................")
		self.ssh_connect.send('copy running-config tftp:\n')
		time.sleep(1)
		out = self.ssh_connect.recv(1024).decode()
		if 'Address of remote host []?'in out:
			logger.info("TFTP Server?172.168.1.17")
			self.ssh_connect.send('172.168.1.17\n')
			time.sleep(1)
			out = self.ssh_connect.recv(1024).decode()
			if 'Destination filename []?' in out:
				date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
				filename = "ruijie"+date+".cfg"
				logger.info("备份文件名%s",filename)
				self.ssh_connect.send(filename+'\n')
				time.sleep(1)
				out = self.ssh_connect.recv(1024).decode()
				if "Transmission success" in out:
					logger.info("%s 备份成功",self.hostname)

		#reout = re.search("(\[(.*?)\][#|$]+)(?P<num>(.*)+)(\[(.*?)\][#|$]+) ", out, re.S)

		self.del_ssh_connect()


class H3cSW:

	def __init__(self, hostname, ip, port, user, password):
		self.hostname = hostname
		self.ip = ip
		self.port = port
		self.user = user
		self.password = password
		self.client = None
		self.ssh_connect = None

	def new_ssh_connect(self):
		self.client = paramiko.SSHClient()
		self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		try:
			self.client.connect(self.ip, self.port, self.user, self.password, timeout=5)
			self.ssh_connect = self.client.invoke_shell()
		except Exception as e:
			logger.error("设备%s登陆失败，失败原因：%s", self.hostname, e)
			exit()

	def del_ssh_connect(self):
		self.client.close()
		logger.info("%s 已断开连接",self.hostname)

	def to_system_view(self):
		self.ssh_connect.send('systemview\n')
		time.sleep(1)
		out = self.ssh_connect.recv(1024).decode()
		if "Password:" in out:
			self.ssh_connect.send('wangluo123\n')
			time.sleep(1)
			out = self.ssh_connect.recv(1024).decode()
			if "Password:" in out:
				print("enable 密码错误，请核对！！！")
			elif "Ruijie#" in out:
				print("enable 密码正确 ，进入enable模式")

	def display_cu(self):
		out = self.ssh_connect.recv(1024).decode()
		print(out)
		print("11")
		self.ssh_connect.send('display cu \n')
		time.sleep(1)
		out = self.ssh_connect.recv(1024).decode()
		conf = out
		while "Ruijie#" not in out:
			self.ssh_connect.send('  ')
			out = self.ssh_connect.recv(1024).decode()
			conf = conf + out

	def display_mac(self):
		self.ssh_connect.send('display mac \n')
		time.sleep(1)
		out = self.ssh_connect.recv(1024).decode()
		conf = out
		while "Ruijie#" not in out:
			self.ssh_connect.send('  ')
			out = self.ssh_connect.recv(1024).decode()
			conf = conf + out
		print(conf)

	def show_arp(self):
		self.ssh_connect.send('display arp \n')
		time.sleep(1)
		out = self.ssh_connect.recv(1024).decode()
		conf = out
		while "Ruijie#" not in out:
			self.ssh_connect.send('  ')
			out = self.ssh_connect.recv(1024).decode()
			conf = conf + out
		print(conf)

	def conf_bak(self):

		self.new_ssh_connect()
		time.sleep(1)
		out = self.ssh_connect.recv(1024).decode()
		#fencoding = chardet.detect(out)
		date = datetime.datetime.now().strftime("%Y%m%d")
		filename = self.hostname+"-"+date+".cfg"
		cmd = "backup startup-configuration to 10.16.17.100 "+filename
		self.ssh_connect.send( "\n")
		time.sleep(1)
		self.ssh_connect.send(cmd+"\n")
		time.sleep(5)
		out = self.ssh_connect.recv(65535).decode()
		if 'Finished.'or 'finished!' in out:
			logger.info("%s 备份成功",self.hostname)
		else:
			logger.error("%s 备份失败",self.hostname)
		self.del_ssh_connect()

if __name__ == '__main__':

	# Excel读取备份列表
	devxls = xlrd.open_workbook("netlist.xlsx")
	devsheet = devxls.sheet_by_index(0)

	for i in range(1,devsheet.nrows):
		devtype = devsheet.cell_value(i,0)
		hostname = devsheet.cell_value(i, 1)
		ip = devsheet.cell_value(i, 2)
		port = devsheet.cell_value(i, 3)
		username = devsheet.cell_value(i, 4)
		password = devsheet.cell_value(i, 5)
		print(port)
		if devtype == 'h3c':
			lt = H3cSW(hostname, ip, port, username, password)
			bak_thread = threading.Thread(target=lt.conf_bak)
			bak_thread.start()


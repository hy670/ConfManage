# -*- coding:utf8 -*-
import IPy
import re
from ConfManage.utils.logger import logger


# 地址对象
class Addr:
	def __init__(self, addrid="", name=""):
		self.addrid = addrid
		self.name = name
		self.addrcontent = []

	# 地址对象增加IP
	def addaddrcontent(self, content):
		self.addrcontent.append(content)

	# 打印地址对象
	def printaddress(self):
		print('address name :' + self.name)
		for i in range(len(self.addrcontent)):
			print(' ' + self.addrcontent[i])


# 地址组对象
class AddrGrp:
	def __init__(self, addrgrpid="", name=""):
		self.addrgrpid = addrgrpid
		self.name = name
		self.addressobject = []

	def addaddressobject(self, content):
		self.addressobject.append(content)

	# 打印地址组
	def printaddrgrp(self):
		print('addressgroup name :' + self.name)
		for i in range(len(self.addressobject)):
			print(' ' + self.addressobject[i])


# 策略中添加多个地址对象自动生成的地址组对象，内容可是地址对象或地址组对象
class RuleAddrGrp:
	def __init__(self, ruleaddrgrpid="", name=""):
		self.ruleaddrgrpid = ruleaddrgrpid
		self.name = name
		self.oid = []
		self.gid = []


# 服务对象
class Ser:
	def __init__(self, serid="", name=""):
		self.serid = serid
		self.name = name
		self.servicecontent = []

	# 增加服务对象内容（协议号，端口号）
	def addservicecontent(self, content):
		self.servicecontent.append(content)

	# 打印服务对象
	def printser(self):
		print('service name :' + self.name)
		for i in range(len(self.servicecontent)):
			print(self.servicecontent[i])


# 默认服务对象，知名端口服务
class DefaultSer:
	def __init__(self, defaultserid="", name=""):
		self.defaultserid = defaultserid
		self.name = name
		self.defaultsercontent = []

	# 打印默认服务
	def printdefaultser(self):
		print('defaultservice id :' + self.defaultserid)
		print('defaultservice name :' + self.name)
		for i in range(len(self.defaultsercontent)):
			print(self.defaultsercontent[i])


# 服务组
class ServGrp:
	def __init__(self, sergrpid="", name=""):
		self.sergrpid = sergrpid
		self.name = name
		self.serviceobject = []

	#  增加服务组的服务对象
	def addserviceobject(self, content):
		self.serviceobject.append(content)

	# 打印服务组
	def printservicegroup(self):
		print('servicegroup name :' + self.name)
		for i in range(len(self.serviceobject)):
			print(self.serviceobject[i])


#  策略中添加多个服务对象自动生成的服务组对象，内容可是服务对象或服务组对象
class RuleServGrp:
	def __init__(self, rulesergrpid="", name=""):
		self.rulesergrpid = rulesergrpid
		self.name = name
		self.membername = []

	# 打印策略服务组
	def printrulesergrp(self):
		print('ruleservicegroup name :' + self.name)
		for i in range(len(self.membername)):
			print(self.membername[i])


# 初始策略
class Policy:
	def __init__(self, policyid="", name=""):
		self.policyid = policyid
		self.name = name
		self.policycontent = {}

	def printpolicy(self):
		print('policy id :' + self.policyid)
		print('policy name :' + self.name)
		print(' policy detail:')
		print(self.policycontent)


class PolicyDetail:
	def __init__(self, id='', name=""):
		self.policyid = id
		self.name = name
		self.srceth = ''
		self.dsteth = ''
		self.srcaddr = []
		self.dstaddr = []
		self.service = []

	def printpolicydetail(self) -> object:
		print('policydetail id :' + self.policyid, end=" ")
		print('name :' + self.name, end=" ")
		print('  srceth :' + self.srceth, end=" ")
		print('  dsteth :' + self.dsteth, end=" ")
		print('  srcaddr :', end=" ")
		for i in range(len(self.srcaddr)):
			print('  ' + self.srcaddr[i], end=" ")
		print(' policydetail dstaddr :', end=" ")
		for i in range(len(self.dstaddr)):
			print('  ' + self.dstaddr[i], end=" ")
		print(' policydetail service :', end=" ")
		for i in range(len(self.service)):
			print('  ' + str(self.service[i]), end=" ")
		print('\n')


class PolicyMic:
	def __init__(self, id='', name=""):
		self.policyid = id
		self.name = name
		self.srceth = ''
		self.dsteth = ''
		self.srcaddr = ''
		self.dstaddr = ''
		self.service = {}

	def printpolicymic(self):
		print('policymic id :' + self.policyid, end=" ")
		print('name :' + self.name, end=" ")
		print('  srceth :' + self.srceth, end=" ")
		print('  dsteth :' + self.dsteth, end=" ")
		print('  srcaddr :', end=" ")
		print('  ' + self.srcaddr, end=" ")
		print('  dstaddr :', end=" ")
		print('  ' + self.dstaddr, end=" ")
		print(' service :', end=" ")
		print('  ' + str(self.service))


class USG4000EP:
	def __init__(self, id="", name="",conf_cwd="./conffile/usg.conf"):
		self.assetid = id
		self.name = name
		self.type = 'firewall'
		self.portlink = ['internet-互联网电信', 'intranet-WWFW-M']
		self.conf_cwd =conf_cwd
		self.zone = []
		self.addrlist = []
		self.addrgrplist = []
		self.ruleaddrgrplist = []
		self.serlist = []
		self.defaultserlist = []
		self.sergrplist = []
		self.rulesergrplist = []
		self.policylist = []
		self.policydetaillist = []
		self.policymiclist = []
		self.parseconffile(self.conf_cwd)
		self.creatpolicydetail()
		self.creatpolicymic()

	def locataddrbyid(self, addrid):
		for i in self.addrlist:
			if addrid == i.addrid:
				return i
		return 0

	def locataddrbyname(self, addrname):
		for i in self.addrlist:
			if addrname == i.name:
				return i
		return 0

	def locataddrgrpbyid(self, addrgrpid):
		for i in self.addrgrplist:
			if addrgrpid == i.addrgrpid:
				return i
		return 0

	def locataddrgrpbyname(self, name):
		for i in self.addrgrplist:
			if name == i.name:
				return i
		return 0

	def locatruleaddrgrpbyid(self, ruleaddrgrpid):

		for i in self.ruleaddrgrplist:
			if ruleaddrgrpid == i.ruleaddrgrpid:
				return i
		return 0

	def locatruleaddrgrpbyname(self, name):
		for i in self.ruleaddrgrplist:
			if name == i.name:
				return i
		return 0

	def locatserbyid(self, serid):
		for i in self.serlist:
			if serid == i.serid:
				return i
		return 0

	def locatserbyname(self, name):
		for i in self.serlist:
			if name == i.name:
				return i
		return 0

	def locatdefaultserbyid(self, serid):
		for i in self.defaultserlist:
			if serid == i.defaultserid:
				return i
		return 0

	def locatdefaultserbyname(self, name):
		for i in self.defaultserlist:
			if name == i.name:
				return i
		return 0

	def locatsergrpbyid(self, sergrpid):
		for i in self.sergrplist:
			if sergrpid == i.sergrpid:
				return i
		return 0

	def locatsergrpbyname(self, name):
		for i in self.sergrplist:
			if name == i.name:
				return i
		return 0

	def locatrulesergrpbyid(self, rulesergrpid):
		for i in self.rulesergrplist:
			if rulesergrpid == i.rulesergrpid:
				return i
		return 0

	def locatrulesergrpbyname(self, name):
		for i in self.rulesergrplist:
			if name == i.name:
				return i
		return 0

	# 生成策略标准五元组

	def creatpolicydetail(self):
		for i in self.policylist:
			policydic = i.policycontent
			if policydic['type'] == '1':
				temppolicydetail = PolicyDetail(i.policyid, i.name)
				temppolicydetail.srceth = policydic['izone']
				temppolicydetail.dsteth = policydic['ozone']
				if policydic['saddrtype'] == '9':
					tempruleaddrgrp = self.locatruleaddrgrpbyid(policydic['saddrid'])
					if tempruleaddrgrp != 0:
						if tempruleaddrgrp.oid:
							for i in tempruleaddrgrp.oid:
								tempaddr = self.locataddrbyid(i)
								for i in tempaddr.addrcontent:
									temppolicydetail.srcaddr.append(i)
						if tempruleaddrgrp.gid:
							for i in tempruleaddrgrp.gid:
								tempaddrgrp = self.locataddrgrpbyid(i)
								for j in tempaddrgrp.addressobject:
									tempaddr = self.locataddrbyid(j)
									for i in tempaddr.addrcontent:
										temppolicydetail.srcaddr.append(i)
				elif policydic['saddrtype'] == '7':
					if policydic['saddrid'] == '0':
						tempaddr = self.locataddrbyid('1')
					else:
						tempaddr = self.locataddrbyid(policydic['saddrid'])
					for i in tempaddr.addrcontent:
						temppolicydetail.srcaddr.append(i)
				else:
					pass
				if policydic['daddrtype'] == '9':
					tempruleaddrgrp = self.locatruleaddrgrpbyid(policydic['daddrid'])
					if tempruleaddrgrp != 0:
						if tempruleaddrgrp.oid:
							for i in tempruleaddrgrp.oid:
								tempaddr = self.locataddrbyid(i)
								for j in tempaddr.addrcontent:
									temppolicydetail.dstaddr.append(j)
						if tempruleaddrgrp.gid:
							for i in tempruleaddrgrp.gid:
								tempaddrgrp = self.locataddrgrpbyid(i)
								for j in tempaddrgrp.addressobject:
									tempaddr = self.locataddrbyid(j)
									for i in tempaddr.addrcontent:
										temppolicydetail.dstaddr.append(i)
				elif policydic['daddrtype'] == '7':
					if policydic['daddrid'] == '0':
						tempaddr = self.locataddrbyid('1')
					else:
						tempaddr = self.locataddrbyid(policydic['daddrid'])
					for i in tempaddr.addrcontent:
						temppolicydetail.dstaddr.append(i)
				else:
					pass
				if policydic['servicetype'] == '6':
					if policydic['serviceid'] == '0':
						tempdefaultser = self.locatdefaultserbyid('1')
					else:
						tempdefaultser = self.locatdefaultserbyid(policydic['serviceid'])
					for i in tempdefaultser.defaultsercontent:
						temppolicydetail.service.append(i)
				elif policydic['servicetype'] == '4':
					tempser = self.locatserbyid(policydic['serviceid'])
					for i in tempser.servicecontent:
						temppolicydetail.service.append(i)
				elif policydic['servicetype'] == '7':
					temprulesergrp = self.locatrulesergrpbyid(policydic['serviceid'])
					for i in temprulesergrp.membername:
						tempdefaultser = self.locatdefaultserbyname(i)
						tempser = self.locatserbyname(i)
						if tempser != 0:
							for j in tempser.servicecontent:
								temppolicydetail.service.append(j)
						else:
							for j in tempdefaultser.defaultsercontent:
								temppolicydetail.service.append(j)
				elif policydic['servicetype'] == '1':
					tempdefaultser = self.locatdefaultserbyid(policydic['serviceid'])
					for i in tempdefaultser.defaultsercontent:
						temppolicydetail.service.append(i)
				else:
					pass
				self.policydetaillist.append(temppolicydetail)
			else:
				msg = "USG策略类型：" + policydic['type'] + "未解析"
				logger.debug(msg=msg)

	def creatpolicymic(self):
		for i in self.policydetaillist:
			for j in i.srcaddr:
				for k in i.dstaddr:
					for l in i.service:
						tempmetapolicy = PolicyMic(i.policyid, i.name)
						tempmetapolicy.srceth = i.srceth
						tempmetapolicy.dsteth = i.dsteth
						tempmetapolicy.srcaddr = j
						tempmetapolicy.dstaddr = k
						tempmetapolicy.service = l
						self.policymiclist.append(tempmetapolicy)

	def parseconffile(self,conf_cwd):
		f = open(conf_cwd, 'r', encoding="UTF-8")
		linedone = 0
		linemum = 0
		while not linedone:
			linemum = linemum + 1
			# 异常捕获 启明防火墙配置文件中有异常编码，UTF-8无法解析
			try:
				line = f.readline()
			except Exception as e:
				logger.warn("第%d行错误:%s", linemum, e)
				continue
			# 判断是否文件结尾
			if line != "":
				key = line.strip().split(' ', 3)
				if len(key) > 2:
					# 解析服务对象
					if key[1] == 'service' and key[2] == "service":
						# 引号内容不分割
						tokss = re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', line.strip())
						# 初始化服务对象
						tempser = Ser(tokss[4].split('"')[1], tokss[8].split('"')[1])
						serdic = {}
						# 解析协议及端口
						for i in range(9, len(tokss) - 2, 2):
							serdic[tokss[i]] = tokss[i + 1].split('"')[1]
						for i in range(1, 8):
							tempstr = 'protocol' + str(i)
							# 服务组可包含8个端口，protocol1-8 如protocolX 的值为256，则未启用
							if serdic[tempstr] != "256":
								if (serdic['dlport' + str(i)]) == (serdic['dhport' + str(i)]):
									portdic = {}
									portdic['port'] = serdic['dlport' + str(i)]
									portdic['protocol'] = serdic['protocol' + str(i)]
									tempser.servicecontent.append(portdic)
								else:
									for j in range(int(serdic['dlport' + str(i)]), int(serdic['dhport' + str(i)]) + 1):
										portdic = {}
										portdic['port'] = str(j)
										portdic['protocol'] = serdic['protocol' + str(i)]
										tempser.servicecontent.append(portdic)
						self.serlist.append(tempser)
					# 解析默认服务对象
					elif key[1] == 'service' and key[2] == "defaultservice":
						tokss = re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', line.strip())
						# 初始化默认服务组 ID、名称
						tempdefaultser = DefaultSer(tokss[4].split('"')[1], tokss[8].split('"')[1])
						defaultserdic = {}
						for i in range(9, len(tokss) - 2, 2):
							defaultserdic[tokss[i]] = tokss[i + 1].split('"')[1]
						tempdefaultser.defaultsercontent.append(
							{'port': defaultserdic['port'], 'protocol': defaultserdic['protocol']})
						self.defaultserlist.append(tempdefaultser)
					# 解析服务组对象 基本没有使用 未实现
					elif key[1] == 'service' and key[2] == "servicegrp":
						tokss = re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', line.strip())
						tempsergrp = ServGrp(tokss[4].split('"')[1], tokss[8].split('"')[1])
						sergrpdic = {}
						for i in range(9, len(tokss) - 2, 2):
							sergrpdic[tokss[i]] = tokss[i + 1].split('"')[1]
					# 解析策略服务组
					elif key[1] == 'service' and key[2] == "ruleservgrp":
						tokss = re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', line.strip())
						# 初始化策略服务组 id、名称
						temprulesergrp = RuleServGrp(tokss[4].split('"')[1], tokss[8].split('"')[1])
						rulesergrpdic = {}
						for i in range(9, len(tokss), 2):
							rulesergrpdic[tokss[i]] = tokss[i + 1].split('"')[1]
						for i in rulesergrpdic['membername'].split(';'):
							temprulesergrp.membername.append(i)
						self.rulesergrplist.append(temprulesergrp)
					# 解析地址对象
					elif key[1] == 'address' and key[2] == "address":
						tokss = re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', line.strip())
						tempaddr = Addr(tokss[4].split('"')[1], tokss[8].split('"')[1])
						addrdic = {}
						for i in range(9, len(tokss) - 2, 2):
							addrdic[tokss[i]] = tokss[i + 1].split('"')[1]
						if addrdic['type'] == '1':
							tempaddr.addrcontent.append(str(IPy.IP(addrdic['ip'], make_net=True)))
						elif addrdic['type'] == '2':
							addrlh = addrdic['ip'].split('-')
							addrl = addrlh[0]
							addrh = addrlh[1]
							addrlsplit = addrl.split('.')
							addrhsplit = addrh.split('.')
							if addrlsplit[0] != addrhsplit[0]:
								pass
							elif addrlsplit[1] != addrhsplit[1]:
								pass
							elif addrlsplit[2] != addrhsplit[2]:
								pass
							elif addrlsplit[3] != addrhsplit[3]:
								for i in range(int(addrlsplit[3]), int(addrhsplit[3]) + 1):
									ipstr = addrlsplit[0] + "." + addrlsplit[1] + "." + addrlsplit[2] + "." + str(i)
									tempaddr.addrcontent.append(ipstr)
						elif addrdic['type'] == '3':
							for j in addrdic['ip'].split(';'):
								tempaddr.addrcontent.append(str(IPy.IP(j, make_net=True)))
						self.addrlist.append(tempaddr)
					# 解析地址组对象
					elif key[1] == 'address' and key[2] == "addrgrp":
						tokss = re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', line.strip())
						temaddrgrp = AddrGrp(tokss[4].split('"')[1], tokss[8].split('"')[1])
						addrgrpdic = {}
						for i in range(9, len(tokss) - 2, 2):
							addrgrpdic[tokss[i]] = tokss[i + 1].split('"')[1]
						addrID = addrgrpdic['o_id'].split(';')
						for i in addrID:
							temaddrgrp.addressobject.append(i)
						self.addrgrplist.append(temaddrgrp)
					# 解析策略地址组对象
					elif key[1] == 'address' and key[2] == "ruleaddrgrp":
						tokss = re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', line.strip())
						tempruleaddrgrp = RuleAddrGrp(tokss[4].split('"')[1], tokss[10].split('"')[1])
						ruleaddrgrpdic = {}
						for i in range(11, len(tokss), 2):
							ruleaddrgrpdic[tokss[i]] = tokss[i + 1].split('"')[1]
						if ruleaddrgrpdic['o_id']:
							for itemruleaddrgrp in ruleaddrgrpdic['o_id'].split(';'):
								tempruleaddrgrp.oid.append(itemruleaddrgrp)
						if ruleaddrgrpdic['g_id']:
							tempruleaddrgrp.gid.append(ruleaddrgrpdic['g_id'])
						self.ruleaddrgrplist.append(tempruleaddrgrp)
					# 解析策略
					elif key[1] == 'rule' and key[2] == "policyinfo":
						tokss = re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', line.strip())
						temppolicy = Policy(tokss[4].split('"')[1], tokss[8].split('"')[1])
						policydic = {}
						for i in range(9, len(tokss) - 2, 2):
							policydic[tokss[i]] = tokss[i + 1].split('"')[1]
						temppolicy.policycontent = policydic
						self.policylist.append(temppolicy)
					elif key[1] == 'seczone':
						tokss = re.split(' ', line.strip())
						self.zone.append(re.split('"', tokss[4])[1])
			else:
				linedone = 1
		f.close()

	def redundantcheck(self):
		number = 1
		policydiclist = []
		for i in range(len(self.policymiclist)):
			for j in range(i + 1, len(self.policymiclist)):
				if self.policymiclist[i].policyid != self.policymiclist[j].policyid:
					if self.policymiclist[i].srceth == self.policymiclist[j].srceth and \
							self.policymiclist[i].dsteth == self.policymiclist[j].dsteth:
						if IPy.IP(self.policymiclist[i].srcaddr).overlaps(self.policymiclist[j].srcaddr) == 1 or \
								IPy.IP(self.policymiclist[j].srcaddr).overlaps(self.policymiclist[i].srcaddr) == 1:
							if IPy.IP(self.policymiclist[i].dstaddr).overlaps(self.policymiclist[j].dstaddr) == 1 or \
									IPy.IP(self.policymiclist[j].dstaddr).overlaps(self.policymiclist[i].dstaddr) == 1:
								if self.policymiclist[i].service['protocol'] == '0' or self.policymiclist[j].service[
									'protocol'] == '0':
									temppolicydic1 = {'number': number, 'dev': self.name,
													  'id': self.policymiclist[i].policyid,
													  'srceth': self.policymiclist[i].srceth,
													  'dsteth': self.policymiclist[i].dsteth,
													  'srcaddr': self.policymiclist[i].srcaddr,
													  'dstaddr': self.policymiclist[i].dstaddr,
													  'protocol': self.policymiclist[i].service['protocol'],
													  'port': self.policymiclist[i].service['port']}
									temppolicydic2 = {'number': number, 'dev': self.name,
													  'id': self.policymiclist[j].policyid,
													  'srceth': self.policymiclist[j].srceth,
													  'dsteth': self.policymiclist[j].dsteth,
													  'srcaddr': self.policymiclist[j].srcaddr,
													  'dstaddr': self.policymiclist[j].dstaddr,
													  'protocol': self.policymiclist[j].service['protocol'],
													  'port': self.policymiclist[j].service['port']}
									policydiclist.append(temppolicydic1)
									policydiclist.append(temppolicydic2)
									number = number + 1
								elif self.policymiclist[i].service['protocol'] == self.policymiclist[j].service[
									'protocol']:
									if self.policymiclist[i].service['port'] == self.policymiclist[j].service['port']:
										temppolicydic1 = {'number': number, 'dev': self.name,
														  'id': self.policymiclist[i].policyid,
														  'srceth': self.policymiclist[i].srceth,
														  'dsteth': self.policymiclist[i].dsteth,
														  'srcaddr': self.policymiclist[i].srcaddr,
														  'dstaddr': self.policymiclist[i].dstaddr,
														  'protocol': self.policymiclist[i].service['protocol'],
														  'port': self.policymiclist[i].service['port']}
										temppolicydic2 = {'number': number, 'dev': self.name,
														  'id': self.policymiclist[j].policyid,
														  'srceth': self.policymiclist[j].srceth,
														  'dsteth': self.policymiclist[j].dsteth,
														  'srcaddr': self.policymiclist[j].srcaddr,
														  'dstaddr': self.policymiclist[j].dstaddr,
														  'protocol': self.policymiclist[j].service['protocol'],
														  'port': self.policymiclist[j].service['port']}
										policydiclist.append(temppolicydic1)
										policydiclist.append(temppolicydic2)
										number = number + 1
		return policydiclist

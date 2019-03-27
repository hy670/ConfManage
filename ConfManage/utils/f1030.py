# -*- coding:utf8 -*-
import IPy
import re
import os


class Addr:
	def __init__(self, name=""):
		self.name = name
		self.addrcontent = []

	def addaddrcontent(self, content):
		self.addrcontent.append(content)

	def printaddress(self):
		print('address name :' + self.name)
		for i in range(len(self.addrcontent)):
			print(' ' + self.addrcontent[i])


class Ser:
	def __init__(self, name=""):
		self.name = name
		self.sercontent = []

	def addservicecontent(self, content):
		self.sercontent.append(content)

	def printser(self):
		print('service name :' + self.name)
		for i in self.sercontent:
			print(i)


class Policy:
	def __init__(self, name=""):

		self.name = name
		self.srceth = ''
		self.dsteth = ''
		self.srcaddr = []
		self.dstaddr = []
		self.service = []

	def printpolicy(self):
		print('policy name :' + self.name)
		print(' policy srceth :' + self.srceth)
		print(' policy dsteth :' + self.dsteth)
		print(' policy srcaddr :')
		for i in range(len(self.srcaddr)):
			print('  ' + self.srcaddr[i])
		print(' policy dstaddr :')
		for i in range(len(self.dstaddr)):
			print('  ' + self.dstaddr[i])
		print(' policy service :')
		for i in range(len(self.service)):
			print('  ' + str(self.service[i]))


class PolicyMic:
	def __init__(self, id='', name=""):
		self.policyid = id
		self.name = name
		self.srceth = ''
		self.dsteth = ''
		self.srcaddr = ''
		self.dstaddr = ''
		self.service = {}

	def printpolicymic(self) -> object:
		print('policydetail id :' + self.policyid, end=" ")
		print('name :' + self.name, end=" ")
		print('  srceth :' + self.srceth, end=" ")
		print('  dsteth :' + self.dsteth, end=" ")
		print('  srcaddr :', end=" ")
		print('  ' + self.srcaddr, end=" ")
		print(' dstaddr :', end=" ")
		print('  ' + self.dstaddr, end=" ")
		print(' policydetail service :', end=" ")
		print('  ' + str(self.service))


class F1030:
	def __init__(self, name=""):
		self.name = name
		self.type = 'firewall'
		self.portlink = ['DB-dbaddr', 'APP-appaddr', 'VPN-jtaddr', 'VPN-wzaddr', 'extranet-hxsw']
		self.addrlist = []
		self.addrgrplist = []
		self.ruleaddrgrplist = []
		self.serlist = []
		self.defaultserlist = []
		self.sergrplist = []
		self.rulesergrplist = []
		self.policylist = []
		self.policymiclist = []
		self.parseconffile()
		self.creatpolicymic()

	def locataddrbyname(self, addrname):
		for i in self.addrlist:
			if addrname == i.name:
				return i
		return 0

	def locataddrgrpbyname(self, name):
		for i in self.addrgrplist:
			if name == i.name:
				return i
		return 0

	def locatruleaddrgrpbyname(self, name):
		for i in self.ruleaddrgrplist:
			if name == i.name:
				return i
		return 0

	def locatserbyname(self, name):
		for i in self.serlist:
			if name == i.name:
				return i
		return 0

	def locatdefaultserbyname(self, name):
		for i in self.defaultserlist:
			if name == i.name:
				return i
		return 0

	def locatsergrpbyname(self, name):
		for i in self.sergrplist:
			if name == i.name:
				return i
		return 0

	def locatrulesergrpbyname(self, name):
		for i in self.rulesergrplist:
			if name == i.name:
				return i
		return 0

	# 生成策略标准五元组

	def creatpolicymic(self):
		for i in self.policylist:
			tempsrcaddrcontent = []
			tempdstaddrcontent = []
			tempsercontent = []
			if i.srcaddr[0] == 'any':
				tempsrcaddrcontent.append('0.0.0.0/0')
			else:
				for j in i.srcaddr:
					tempsrcaddr = self.locataddrbyname(j)
					for addrcontent in tempsrcaddr.addrcontent:
						tempsrcaddrcontent.append(addrcontent)
			if i.dstaddr[0] == 'any':
				tempdstaddrcontent.append('0.0.0.0/0')
			else:
				for j in i.dstaddr:
					tempdstaddr = self.locataddrbyname(j)
					for addrcontent in tempdstaddr.addrcontent:
						tempdstaddrcontent.append(addrcontent)
			if i.service[0] == 'any':
				tempsercontent.append({'protocol': '0', 'port': '-1'})
			else:
				for j in i.service:
					tempservice = self.locatserbyname(j)
					if j =="LZweblogicport":

						print(tempservice.sercontent)
					if tempservice != 0:
						for sercontent in tempservice.sercontent:
							tempsercontent.append(sercontent)
					else:
						tempsercontent.append({'protocol': '-1', 'port': '0'})
			if not tempdstaddrcontent:
				pass
			if not tempsrcaddrcontent:
				pass
			if not tempsercontent:
				pass
			for j in tempsrcaddrcontent:
				for k in tempdstaddrcontent:
					for l in tempsercontent:
						temppolicydetail = PolicyMic(i.name)
						temppolicydetail.srceth = i.srceth
						temppolicydetail.dsteth = i.dsteth
						temppolicydetail.srcaddr = j
						temppolicydetail.dstaddr = k
						temppolicydetail.service = l
						self.policymiclist.append(temppolicydetail)

	def parseconffile(self):
		ls = os.getcwd()
		print(ls)
		f = open('./conffile/FW1310.conf', 'r', encoding="GBK")
		key = ''
		for line in f:
			if not line[0].isspace():
				tokks = re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', line.strip())
				if 'object' in line:
					if tokks[0] == 'object-group':
						key = tokks[1]
						if tokks[1] == 'ip':
							tempaddr = Addr(tokks[3])
							self.addrlist.append(tempaddr)
						elif tokks[1] == 'service':
							tempser = Ser(tokks[2])
							self.serlist.append(tempser)
					elif tokks[0] == 'object-policy':
						key = tokks[0].split('-')[1] + ':' + tokks[2]

				else:
					key = ''
			elif key:
				if key == 'ip':
					tokks = line.strip().split(' ')
					if tokks[0].isdigit():
						if tokks[2] == 'host':
							self.addrlist[len(self.addrlist) - 1].addrcontent.append(tokks[4])
						elif tokks[2] == 'subnet':
							ipaddr = tokks[3] + '/' + tokks[4]
							self.addrlist[len(self.addrlist) - 1].addrcontent.append(str(IPy.IP(ipaddr, make_net=True)))
				elif key == 'service':
					tokks = re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', line.strip())
					if tokks[0].isdigit():
						servicedic = {}
						if tokks[2] == 'tcp':
							if tokks[3] == 'destination':
								servicedic = {'protocol': '6', 'port': tokks[5]}
							else:
								continue
						elif tokks[2] == 'udp':
							if tokks[3] == 'destination':
								servicedic = {'protocol': '17', 'port': tokks[5]}
							else:
								continue
						elif tokks[2] == 'icmp':
							servicedic = {'protocol': '1', 'port': '-1'}
						elif tokks[2] == 'group-object':
							servicedic = {'protocol': '-1', 'port': '-1'}

						self.serlist[len(self.serlist) - 1].sercontent.append(servicedic)
				elif 'policy' in key:
					tokks = re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', line.strip())
					policydic = {}
					if tokks[2] == 'pass':
						self.policylist.append(Policy(key.split(':')[1] + tokks[1]))
						self.policylist[len(self.policylist) - 1].srceth = key.split(':')[1].split('-')[0]
						self.policylist[len(self.policylist) - 1].dsteth = key.split(':')[1].split('-')[1]
						for i in range(3, len(tokks), 2):

							if tokks[i] == 'counting' or tokks[i] == 'logging':
								continue
							policydic[tokks[i]] = tokks[i + 1]
						if 'source-ip' in policydic.keys():
							self.policylist[len(self.policylist) - 1].srcaddr.append(policydic['source-ip'])
						else:
							self.policylist[len(self.policylist) - 1].srcaddr.append('any')
						if 'destination-ip' in policydic.keys():
							self.policylist[len(self.policylist) - 1].dstaddr.append(policydic['destination-ip'])
						else:
							self.policylist[len(self.policylist) - 1].dstaddr.append('any')
						if 'service' in policydic.keys():
							self.policylist[len(self.policylist) - 1].service.append(policydic['service'])
						else:
							self.policylist[len(self.policylist) - 1].service.append('any')
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




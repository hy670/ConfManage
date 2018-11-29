# -*- coding:utf8 -*-
import IPy
import re
from ConfManage.utils.defaultserdiclist import DefaultSerDicList
from ConfManage.utils.ipprotocol import IpProtocol


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

class AddrGrp:
	def __init__(self, name=""):
		self.name = name
		self.addressobject = []

	def addaddressobject(self, content):
		self.addressobject.append(content)

	def printaddrgrp(self):
		print('addressgroup name :' + self.name)
		for i in range(len(self.addressobject)):
			print(' ' + self.addressobject[i])

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
		self.service ={}

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


class NSG5000:
	def __init__(self, name=""):
		self.name = name
		self.type = 'firewall'
		self.portlink = ['extranet-WANFW-USG6000EP-M', 'intranet-HXSW-01']
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
					tempsrcaddrgrp = self.locataddrgrpbyname(j)
					if tempsrcaddrgrp != 0:
						for k in tempsrcaddrgrp.addressobject:
							tempsrcaddr = self.locataddrbyname(k)
							for addrcontent in tempsrcaddr.addrcontent:
								tempsrcaddrcontent.append(addrcontent)
					elif tempsrcaddr != 0:
						for addrcontent in tempsrcaddr.addrcontent:
							tempsrcaddrcontent.append(addrcontent)
			if i.dstaddr[0] == 'any':
				tempdstaddrcontent.append('0.0.0.0/0')
			else:
				for j in i.dstaddr:
					tempdstaddr = self.locataddrbyname(j)
					tempdstaddrgrp = self.locataddrgrpbyname(j)
					if tempdstaddrgrp !=0:
						for  k in tempdstaddrgrp.addressobject:
							tempdstaddr = self.locataddrbyname(k)
							for addrcontent in tempdstaddr.addrcontent:
								tempdstaddrcontent.append(addrcontent)
					elif tempdstaddr != 0:
						for addrcontent in tempdstaddr.addrcontent:
							tempdstaddrcontent.append(addrcontent)

			for j in i.service:
				tempservice = self.locatserbyname(j)
				if tempservice != 0:
					for sercontent in tempservice.sercontent:
						protocol = str.upper(sercontent['protocol'])

						for line in IpProtocol.ipprotocallist:
							if protocol == line['name']:
								sercontent['protocol'] = line['ipport']
						tempsercontent.append(sercontent)
				else:
					isdefault =0
					for defaultserdic in DefaultSerDicList.defaultserdiclist:
							if j.upper() == defaultserdic['servicename']:
									isdefault =1
									tempsercontent.append({'protocol': str(defaultserdic['protocol']), 'port': str(defaultserdic['port'])})
									break
					if isdefault ==0 :
							print(j)
			if not tempdstaddrcontent:
				pass
			if not tempsrcaddrcontent:
				pass
			if  not tempsercontent:
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
		f = open('./conffile/nsg5000/config_OBJ', 'r', encoding="UTF-8")
		key = ''
		for line in f:
			if 'object network address ' in line:
				key = 'address'
				self.addrlist.append(Addr(re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', line.strip())[3].split('"')[1]))
			elif 'object network address-group' in line:
				key = 'addrgrp'
				self.addrgrplist.append(AddrGrp(re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', line.strip())[3].split('"')[1]))
			elif 'object service custom' in line:
				key = 'service'
				self.serlist.append(Ser(re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', line.strip())[3].split('"')[1]))
			elif key == 'address' and  'network-object' in line:
				tokks = re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', line.strip())
				if tokks[2] == 'host':
					self.addrlist[len(self.addrlist)-1].addrcontent.append(tokks[3].split('"')[1])
				elif tokks[2]== 'network':
					self.addrlist[len(self.addrlist) - 1].addrcontent.append(str(IPy.IP(tokks[3]).make_net(tokks[4])))
				elif tokks[2]== 'range':
					addrrange = tokks[3].split('-')
					start = addrrange[0].split('.')
					end = addrrange[1].split('.')
					for i in range(int(start[3]),int(end[3])+1):
						tempaddr = start[0]+'.'+start[1]+'.'+start[2]+'.'+str(i)
						self.addrlist[len(self.addrlist) - 1].addrcontent.append(tempaddr)
			elif key == 'addrgrp' and  'group-object address' in line:
				tokks = re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', line.strip())
				self.addrgrplist[len(self.addrgrplist)-1].addressobject.append(tokks[2].split('"')[1])
			elif key == 'service' and  'service-item' in line:
				tokks = re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', line.strip())
				if tokks[6] == tokks[7]:
					self.serlist[len(self.serlist)-1].sercontent.append({'protocol':tokks[1],'port':tokks[6]})
			elif 'exit'== line.strip():
				key = ''
		fpolicy = open('./conffile/nsg5000/config_FIREWALL', 'r', encoding="UTF-8")
		for  policyline in fpolicy:
			if 'sip' in policyline and 'dip' in policyline:
				tokks = re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', policyline.strip())
				temppolicy = Policy(tokks[2].split('"')[1])
				temppolicy.srceth = tokks[8].split('"')[1]
				temppolicy.dsteth = tokks[10].split('"')[1]
				temppolicy.srcaddr.append(tokks[4].split('"')[1])
				temppolicy.dstaddr.append(tokks[6].split('"')[1])
				temppolicy.service.append(tokks[12].split('"')[1])
				self.policylist.append(temppolicy)
			elif 'append' in policyline:
				tokks = re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', policyline.strip())
				for i in self.policylist:
					if i.name == tokks[2].split('"')[1]:
						if tokks[4] == 'service':
							i.service.append(tokks[5].split('"')[1])
						elif tokks[4] == 'dip':
							i.dstaddr.append(tokks[5].split('"')[1])
						elif tokks[4] == 'sip':
							i.srcaddr.append(tokks[5].split('"')[1])

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
								if self.policymiclist[i].service['protocol'] == '0' or self.policymiclist[j].service['protocol'] == '0':
									temppolicydic1 = {'number':number,'dev': self.name, 'id': self.policymiclist[i].policyid,
									                  'srceth': self.policymiclist[i].srceth,
									                 'dsteth': self.policymiclist[i].dsteth,
									                 'srcaddr': self.policymiclist[i].srcaddr,
									                  'dstaddr':self.policymiclist[i].dstaddr,
									                 'protocol': self.policymiclist[i].service['protocol'],
									                 'port':self.policymiclist[i].service['port']}
									temppolicydic2 = {'number': number, 'dev': self.name, 'id': self.policymiclist[j].policyid,
									                  'srceth': self.policymiclist[j].srceth,
									                  'dsteth': self.policymiclist[j].dsteth,
									                  'srcaddr': self.policymiclist[j].srcaddr, 'dstaddr': self.policymiclist[j].dstaddr,
									                  'protocol': self.policymiclist[j].service['protocol'],
									                  'port': self.policymiclist[j].service['port']}
									policydiclist.append(temppolicydic1)
									policydiclist.append(temppolicydic2)
									number = number + 1
								elif self.policymiclist[i].service['protocol'] == self.policymiclist[j].service['protocol']:
									if self.policymiclist[i].service['port'] == self.policymiclist[j].service['port']:
										temppolicydic1 = {'number': number, 'dev': self.name, 'id': self.policymiclist[i].policyid,
										                  'srceth': self.policymiclist[i].srceth,
										                  'dsteth': self.policymiclist[i].dsteth,
										                  'srcaddr': self.policymiclist[i].srcaddr, 'dstaddr': self.policymiclist[i].dstaddr,
										                  'protocol': self.policymiclist[i].service['protocol'],
										                  'port': self.policymiclist[i].service['port']}
										temppolicydic2 = {'number': number, 'dev': self.name, 'id': self.policymiclist[j].policyid,
										                  'srceth': self.policymiclist[j].srceth,
										                  'dsteth': self.policymiclist[j].dsteth,
										                  'srcaddr': self.policymiclist[j].srcaddr, 'dstaddr': self.policymiclist[j].dstaddr,
										                  'protocol': self.policymiclist[j].service['protocol'],
										                  'port': self.policymiclist[j].service['port']}
										policydiclist.append(temppolicydic1)
										policydiclist.append(temppolicydic2)
										number = number + 1
		return policydiclist
# -*- coding:utf8 -*-
import IPy
import re




class Addr:
	def __init__(self, addrid="", name=""):
		self.addrid = addrid
		self.name = name
		self.addrcontent = []

	def addaddrcontent(self, content):
		self.addrcontent.append(content)

	def printaddress(self):
		print('address name :' + self.name)
		for i in range(len(self.addrcontent)):
			print(' ' + self.addrcontent[i])


class AddrGrp:
	def __init__(self, addrgrpid="", name=""):
		self.addrgrpid = addrgrpid
		self.name = name
		self.addressobject = []

	def addaddressobject(self, content):
		self.addressobject.append(content)

	def printaddrgrp(self):
		print('addressgroup name :' + self.name)
		for i in range(len(self.addressobject)):
			print(' ' + self.addressobject[i])


class RuleAddrGrp:
	def __init__(self, ruleaddrgrpid="", name=""):
		self.ruleaddrgrpid = ruleaddrgrpid
		self.name = name
		self.oid = []
		self.gid = []


class Ser:
	def __init__(self, serid="", name=""):
		self.serid = serid
		self.name = name
		self.servicecontent = []

	def addservicecontent(self, content):
		self.servicecontent.append(content)

	def printser(self):
		print('service name :' + self.name)
		for i in range(len(self.servicecontent)):
			print(self.servicecontent[i])


class DefaultSer:
	def __init__(self, defaultserid="", name=""):
		self.defaultserid = defaultserid
		self.name = name
		self.defaultsercontent = []

	def printdefaultser(self):
		print('defaultservice id :' + self.defaultserid)
		print('defaultservice name :' + self.name)
		for i in range(len(self.defaultsercontent)):
			print( self.defaultsercontent[i])


class ServGrp:
	def __init__(self, sergrpid="", name=""):
		self.sergrpid = sergrpid
		self.name = name
		self.serviceobject = []

	def addserviceobject(self, content):
		self.serviceobject.append(content)

	def printservicegroup(self):
		print('servicegroup name :' + self.name)
		for i in range(len(self.serviceobject)):
			print(self.serviceobject[i])


class RuleServGrp:
	def __init__(self, rulesergrpid="", name=""):
		self.rulesergrpid = rulesergrpid
		self.name = name
		self.membername = []

	def printrulesergrp(self):
		print('ruleservicegroup name :' + self.name)
		for i in range(len(self.membername)):
			print(self.membername[i])


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
		print('policydetail id :' + self.name)
		print(' policydetail srceth :' + self.srceth)
		print(' policydetail dsteth :' + self.dsteth)
		print(' policydetail srcaddr :')
		for i in range(len(self.srcaddr)):
			print('  ' + self.srcaddr[i])
		print(' policydetail dstaddr :')
		for i in range(len(self.dstaddr)):
			print('  ' + self.dstaddr[i])
		print(' policydetail service :')
		for i in range(len(self.service)):
			print('  ' +  str(self.service[i]))


class PolicyMic:
	def __init__(self, id='', name=""):
		self.policyid = id
		self.name = name
		self.srceth = ''
		self.dsteth = ''
		self.srcaddr = ''
		self.dstaddr = ''
		self.service ={}

	def printpolicymic(self):
		print('policydetail id :' + self.name, end=" ")
		print('  srceth :' + self.srceth, end=" ")
		print('  dsteth :' + self.dsteth, end=" ")
		print('  srcaddr :', end=" ")
		print('  ' + self.srcaddr, end=" ")
		print('  dstaddr :', end=" ")
		print('  ' + self.dstaddr, end=" ")
		print(' service :', end=" ")
		print('  ' + str(self.service))


class USG:
	def __init__(self, name=""):
		self.name = name
		self.type = 'firewall'
		self.portlink = ['internet-internetaddr', 'intranet-nsg5000']
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
		self.parseconffile()
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
								for i in tempaddr.addrcontent:
									temppolicydetail.dstaddr.append(i)
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

	def creatpolicymic(self):
		for i in self.policydetaillist:
			for j in i.srcaddr:
				for k in i.dstaddr:
					for l in i.service:
						tempmetapolicy = PolicyMic(i.policyid,i.name)
						tempmetapolicy.srceth = i.srceth
						tempmetapolicy.dsteth = i.dsteth
						tempmetapolicy.srcaddr = j
						tempmetapolicy.dstaddr = k
						tempmetapolicy.service = l
						self.policymiclist.append(tempmetapolicy)

	def printmetapolicylist(self):
		for i in self.metapolicylist:
			print("policy id:" + i.name + " srceth:" + i.srceth +
			      " dsteth:" + i.dsteth + " srcaddr:" + i.srcaddr + " dstaddr:" + i.dstaddr + " service:" + i.service)

	def parseconffile(self):
		f = open('./conffile/usg.conf', 'r', encoding="UTF-8")
		for line in f:
			key = line.strip().split(' ',3)
			if len(key) > 2:
				if key[1] == 'service' and key[2] == "service":
					tokss = re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', line.strip())
					tempser = Ser(tokss[4].split('"')[1], tokss[8].split('"')[1])
					serdic = {}
					for i in range(9, len(tokss) - 2, 2):
						serdic[tokss[i]] = tokss[i + 1].split('"')[1]
					for i in range(1, 8):
						tempstr = 'protocol' + str(i)
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
				elif key[1] == 'service' and key[2] == "defaultservice":
					tokss = re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', line.strip())
					tempdefaultser = DefaultSer(tokss[4].split('"')[1], tokss[8].split('"')[1])
					defaultserdic = {}
					for i in range(9, len(tokss) - 2, 2):
						defaultserdic[tokss[i]] = tokss[i + 1].split('"')[1]
					tempdefaultser.defaultsercontent.append({'port':defaultserdic['port'],'protocol':defaultserdic['protocol']})
					self.defaultserlist.append(tempdefaultser)
				elif key[1] == 'service' and key[2] == "servicegrp":
					print(line.strip())
					tokss = re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', line.strip())
					tempsergrp = ServGrp(tokss[4].split('"')[1], tokss[8].split('"')[1])
					sergrpdic = {}
					for i in range(9, len(tokss) - 2, 2):
						sergrpdic[tokss[i]] = tokss[i + 1].split('"')[1]
				elif key[1] == 'service' and key[2] == "ruleservgrp":
					tokss = re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', line.strip())
					temprulesergrp = RuleServGrp(tokss[4].split('"')[1], tokss[8].split('"')[1])
					rulesergrpdic = {}
					for i in range(9, len(tokss), 2):
						rulesergrpdic[tokss[i]] = tokss[i + 1].split('"')[1]
					for i in rulesergrpdic['membername'].split(';'):
						temprulesergrp.membername.append(i)
					self.rulesergrplist.append(temprulesergrp)
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
				elif key[1] == 'address' and key[2] == "ruleaddrgrp":
					tokss = re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', line.strip())
					tempruleaddrgrp = RuleAddrGrp(tokss[4].split('"')[1], tokss[10].split('"')[1])
					ruleaddrgrpdic = {}
					for i in range(11, len(tokss), 2):
						ruleaddrgrpdic[tokss[i]] = tokss[i + 1].split('"')[1]
					if ruleaddrgrpdic['o_id']:
						tempruleaddrgrp.oid.append(ruleaddrgrpdic['o_id'])
					if ruleaddrgrpdic['g_id']:
						tempruleaddrgrp.gid.append(ruleaddrgrpdic['g_id'])
					self.ruleaddrgrplist.append(tempruleaddrgrp)
				elif key[1] == 'rule' and key[2] == "policyinfo":
					tokss = re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', line.strip())
					temppolicy = Policy(tokss[4].split('"')[1], tokss[8].split('"')[1])
					policydic = {}
					for i in range(9, len(tokss) - 2, 2):
						policydic[tokss[i]] = tokss[i + 1].split('"')[1]
					temppolicy.policycontent = policydic
					self.policylist.append(temppolicy)
		f.close()

	def redundantcheck(self):
		for i in range(len(self.policymiclist)):
			for j in range(i + 1, len(self.policymiclist)):
				if self.policymiclist[i].name != self.policymiclist[j].name:
					if self.policymiclist[i].srceth == self.policymiclist[j].srceth and \
							self.policymiclist[i].dsteth == self.policymiclist[j].dsteth:
						if IPy.IP(self.policymiclist[i].srcaddr).overlaps(self.policymiclist[j].srcaddr) == 1 or \
								IPy.IP(self.policymiclist[j].srcaddr).overlaps(self.policymiclist[i].srcaddr) == 1:
							if IPy.IP(self.policymiclist[i].dstaddr).overlaps(self.policymiclist[j].dstaddr) == 1 or \
									IPy.IP(self.policymiclist[j].dstaddr).overlaps(self.policymiclist[i].dstaddr) == 1:
								if self.policymiclist[i].service['protocol'] == '-1' or self.policymiclist[j].service['protocol'] == '-1':
									print(str(i) + " " + str(j))
									print("--------------------------------------------------------------")
									self.policymiclist[i].printpolicymic()
									self.policymiclist[j].printpolicymic()
								elif self.policymiclist[i].service['protocol'] == self.policymiclist[j].service['protocol']:
									if self.policymiclist[i].service['port'] == self.policymiclist[j].service['port']:
										print(str(i) +" "+str(j))
										print("--------------------------------------------------------------")
										self.policymiclist[i].printpolicymic()
										self.policymiclist[j].printpolicymic()

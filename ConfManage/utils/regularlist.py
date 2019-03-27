# -*- coding:utf8 -*-

import IPy


class RegularList:
	regularlist = []
	regular = []
	f = open('E:/project/ConfManage/ConfManage/utils/regular/regular.txt', 'r')
	i = 0
	for line in f:
		toos = line.strip().split(" ")
		if toos[3] == 'any':
			toos[3] = '0'
			toos[4] = "-1"
		regular = {"id": i, "name": toos[0], "srcaddr": toos[1], "dstaddr": toos[2], "protocol": toos[3],
				   "port": toos[4], "action": toos[5]}
		regularlist.append(regular)
		i = i + 1
	f.close()

	def regulardelete(number):
		f = open('./ConfManage/utils/regular/regular.txt', 'r+')
		l4 = f.readlines()
		line = int(number)
		l4[line - 1] = ''
		f.close()
		files = open('./ConfManage/utils/regular/regular.txt', 'w+')
		l4 = files.writelines(l4)
		f.close()

	def regularadd(str):
		f = open('./ConfManage/utils/regular/regular.txt', 'a')
		f.write(str + "\n")
		f.close()




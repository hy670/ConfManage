import  re
import pymysql


class DefaultSerDicList:
	defaultserdiclist =[]
	f = open('E:/project/ConfManage/ConfManage/utils/resource/well-known-port', 'r', encoding="UTF-8")
	for line in f:
		key = line.strip().split(' ')
		if len(key)==3:
			defaultserdiclist.append({'servicename':key[0],'protocol':key[1],'port':key[2]})

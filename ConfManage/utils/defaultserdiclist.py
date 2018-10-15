import  re
import pymysql


class DefaultSerDicList:
	defaultserdiclist =[]
	db = pymysql.connect(
		host='127.0.0.1',
		port=12345,
		user='root',
		passwd='12345',
		db='confmgr',
		charset='utf8'
	)
	cur = db.cursor()
	cur.execute("select * from defaultservice")
	results = cur.fetchall()
	for i in results:
		sername = i[0]
		protocol = i[1]
		dstport = i[2]
		defaultserdiclist.append({'servicename':sername,'protocol':protocol,'port':dstport})
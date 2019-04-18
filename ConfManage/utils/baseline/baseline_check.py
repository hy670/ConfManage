section_key = ""
f = open("E:\project\ConfManage\conffile\HXSW-20190417.cfg", 'r', encoding="UTF-8")
for i in f.readlines():
	if not i[0].isspace():
		if i.strip() == '#':
			section_key = ""
		else:
			section_key = i.strip()
	else:
		if not section_key:
			if "snmp" in i:
				print(i.strip())
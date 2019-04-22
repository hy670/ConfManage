import re
section_key = ""
f = open("E:\project\ConfManage\conffile\HXSW-20190417.cfg", 'r', encoding="UTF-8")
for i in f.readlines():
	if not i[0].isspace():
		if i.strip() == '#':
			section_key = ""
		else:
			section_key = i.strip()

	else:



		str = 'service-type (\w+ )'
		ss= re.findall(str,i)

		if ss:
			for i in ss:
				print(i)
from ConfManage.utils import usg,nsg5000,f1030

usg100 = usg.USG('usg100')
usg100.parseconffile()
usg100.creatpolicydetail()
usg100.creatpolicymic()
for i in usg100.policymiclist:
	i.printpolicymic()
f1030 = f1030.F1030('f1030')
f1030.parseconffile()
f1030.creatpolicydetail()
nsg5000 =nsg5000.NSG5000('nsg5000')
nsg5000.parseconffile()
nsg5000.creatpolicydetail()









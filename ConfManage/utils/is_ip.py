import IPy


def is_ip(address):
	try:
		IPy.IP(address)
		return True
	except Exception as e:
		return False

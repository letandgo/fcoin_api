from apis.fcoin import fcoin
from apis.fcoin_margin import fcoinmargin

class Trader(object):
	def __init__(self, website):
		if website == 'fcoin':
			self.public_key = ''
			self.private_key = ''
			self.tradeapi = fcoin(self.public_key, self.private_key)
		elif website == 'fcoin_margin':
			self.public_key = ''
			self.private_key = ''
			self.tradeapi = fcoinmargin(self.public_key, self.private_key)

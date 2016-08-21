from common.hostmask import *

class User:

	def __init__(self, addr):
		self._address  = addr
		self._hostmask = None

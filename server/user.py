from common.hostmask import *

class User(object):

	def __init__(self, addr):
		self._address  = addr
		self._username = None
		self._nickname = None

	def make_hostmask(self):
		if self._nickname is None or self._username is None:
			return None

		(host, _) = self._address
		return Hostmask(self._nickname, self._username, host)

	@property
	def username(self):
		return self._username

	@username.setter
	def username(self, u):
		self._username = u

	@property
	def nickname(self):
		return self._nickname

	@nickname.setter
	def nickname(self, n):
		self._nickname = n


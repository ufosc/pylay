from common.hostmask import *

class User:

	def is_registered(self):
		raise NotImplementedError

class PendingUser(User):

	def __init__(self, addr):
		self.nickname = None
		self.username = None

		self._hostname = addr

	def is_registered(self):
		return False

	def is_complete(self):
		if self.nickname is None:
			return False
		if self.username is None:
			return False

		return True

	@property
	def hostname(self):
		return self._hostname

class RegisteredUser(User):

	@staticmethod
	def from_pending(pu):
		return RegisteredUser(pu.nickname, pu.username, pu.hostname)

	def __init__(self, nick, user, host):
		self._hostmask = Hostmask(nick, user, host)

	def is_registered(self):
		return True

	@property
	def hostmask(self):
		return self._hostmask

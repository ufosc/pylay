from common.hostmask import *

class User(object):
	"""
	The common traits of a user, with or without all required information.
	"""

	def is_registered(self):
		"""
		This function should be overriden to specifiy whether a host can send
		messages, or still need to send USER/NICK info.

		:return: A boolean representing the registered state.
		"""

		raise NotImplementedError

	@property
	def nickname(self):
		raise NotImplementedError

	@nickname.setter
	def nickname(self, nick):
		raise NotImplementedError

class PendingUser(User):
	"""
	The initial state of a user.
	The user can only leave this state once USER/NICK info is sent.
	"""

	def __init__(self, addr):
		"""
		Create a new pending user.
		The hostname is always available immeadiately.

		:param addr: The hostname of the client.
		:return: None
		"""

		#User.__init__(self)
		self._hostname = addr

		self._nickname = None
		self._username = None

	def is_registered(self):
		return False

	def is_complete(self):
		"""
		A pending user is complete once USER/NICK info is available.
		A user can only be promoted to registered once they are complete.

		:return: A boolean representing whether or not the user is complete.
		"""

		if self._nickname is None:
			return False
		if self._username is None:
			return False

		return True

	@property
	def username(self):
		return self._username

	@username.setter
	def username(self, u):
		self._username = u

	@property
	def hostname(self):
		return self._hostname

	@property
	def nickname(self):
		return self._nickname

	@nickname.setter
	def nickname(self, nick):
		self._nickname = nick

class RegisteredUser(User):
	"""
	A user that has USER/NICK info.
	A registered user can send messages and use the rest of IRC functionality.
	"""

	@staticmethod
	def from_pending(pu):
		"""
		Promote a pending user to a registered user.

		:param pu: The pending user to promote.
		:return: A new registered user with the information of the pending user.
		"""

		return RegisteredUser(pu.nickname, pu.username, pu.hostname)

	def __init__(self, nick, user, host):
		"""
		Create a new registered user with the given identification info.

		:param nick: The user nickname.
		:param user: The user username.
		:param host: The user hostname.
		:return: None
		"""

		#User.__init__(self)
		self._hostmask = Hostmask(nick, user, host)

	def is_registered(self):
		return True

	@property
	def hostmask(self):
		return self._hostmask

	@property
	def nickname(self):
		return self._hostmask.nickname

	@nickname.setter
	def nickname(self, nick):
		self._hostmask.nickname = nick
